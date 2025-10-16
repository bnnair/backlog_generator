
from typing import List, Dict, Any
import asyncio
import json
import re
from utils import get_logger, BaseAppException, LLMError, ValidationError, ConfigManager, progressive_json_repair
from services.llm_manager import AIAdapter
from services.requirement_specialist import RequirementsSpecialist
from services.backlog_specialist import BacklogSpecialist
from models.database import RequirementsDatabase
from factory.ai_model_factory import AIModelFactory   

logger = get_logger(__name__)   





class RequirementsOrchestrator:
    """Simplified orchestrator for requirement document and product backlog generation"""
    
    def __init__(self):
        self.db = RequirementsDatabase()
        # self.llm_adapter = self._initialize_llm_adapter()
        AIModelFactory.initialize()
        self.llm_adapter = AIModelFactory.create_model("deepseek")
        
        self.requirements_agent = RequirementsSpecialist(self.llm_adapter, agent_id="req_agent", db=self.db)
        self.backlog_agent = BacklogSpecialist(self.llm_adapter, agent_id="backlog_agent", db=self.db)
        self.max_iterations = 50  # Maximum feedback cycles
    
    def _initialize_llm_adapter(self) -> AIAdapter:
        """Initialize LLM adapter"""
        try:
            logger.info("Initializing LLM adapter")
            
            MODEL_TYPE = "mistral"  # Options: 'openai', 'deepseek', 'perplexity','huggingface', 'mistral'
            # Call the LLM to enhance the resume
            config = ConfigManager.update_config()
            logger.debug(f"config : {config}")
            aiadapter = AIAdapter(config, MODEL_TYPE)
            logger.debug(f"adapter : {aiadapter}")
            
            return aiadapter
            
        except Exception as e:
            logger.error("Failed to initialize LLM adapter", exception=e)
            raise
    
    
    def is_feedback_empty(self, feedback_data):
        """
        Check if feedback JSON has no suggestions in any category
        """
        if not feedback_data or 'feedback' not in feedback_data:
            return True
        
        feedback = progressive_json_repair(feedback_data)
        feedback = feedback['feedback']
        
        # Check for required_changes array in the new structure
        if 'required_changes' in feedback:
            changes = feedback['required_changes']
            if changes and len(changes) > 0:  # If there are any required changes
                return False
        
        # Also check for empty array case
        if 'required_changes' in feedback and feedback['required_changes'] == []:
            return True
    
    async def generate_feedback_mechanism(self, backlog: str, project_id:int, backlog_id:int, 
                                          iteration_count: int = 0):
        """Generate feedback mechanism for backlog review"""
        try:
            
            logger.info(f"Generating feedback mechanism for backlog functional review")
            # Step 3: Review and refine backlog
            logger.info("Step 3: Reviewing and refining backlog...")
            iteration = 0 + iteration_count
            all_feedback = []
            updated_items = backlog
            while iteration < self.max_iterations:
                iteration += 1
                logger.info(f"  Iteration {iteration} of {self.max_iterations}")

                # BA agent reviews the backlog
                feedback_items = await self.requirements_agent.review_fr_backlog( updated_items, 
                                                    project_id, backlog_id, feedback_id=iteration)

                if self.is_feedback_empty(feedback_items):
                    logger.info("  No feedback - backlog is complete!")
                    break
                
                ## Process feedback JSON for any errors
                feedback_json = None
                try:
                    logger.info("cleaning the feedback json--------------------")
                    feedback = progressive_json_repair(feedback_items)
                    logger.debug(f"Initial LLM feedback parse successful: {json.dumps(feedback, indent=2)}")
                    logger.info("cleaning the backlog json---------------------")
                    updated_items = progressive_json_repair(updated_items)
                    logger.debug(f"the llm backlog parse successfull.")
                except json.JSONDecodeError as e:
                    logger.info(f"Initial parse failed: {e}.")
                    raise ValueError("Could not parse JSON from LLM response")


                feedback_json = json.dumps(feedback['feedback'])
                logger.info(f"Feedback json loaded.........")
                
                all_feedback.append(feedback_json)
                updated_items = json.dumps(updated_items)
                # Backlog specialist addresses the feedback
                updated_items = await self.backlog_agent.improve_fr_backlog( updated_items, feedback_json)
            
                logger.info(f"  Updated backlog items based on feedback : {updated_items}")

                self.db.update_backlog_item(backlog_id, updated_items)
                logger.info(f"  Backlog item updated in database for iteration {iteration}")
                    
            return updated_items, iteration, all_feedback
            
        except BaseAppException as e:
            logger.error("Deliverables generation failed", exception=e)
            return {
                'status': 'failed',
                'error': e.message
            }
        except Exception as e:
            logger.error("Unexpected error during deliverables generation", exception=e)
            return {
                'status': 'failed',
                'error': f'Unexpected system error: {str(e)}'
            }    
    
    async def continue_backlog_gen(self, backlog_id: int = 0) -> str:
        """Continue working on an existing backlog"""
        try:
            logger.info(f"Continuing work on existing backlog ID: {backlog_id}")
            if backlog_id not in [0, None]:
                self.backlog_id = backlog_id
            else:
                ## get the latest backlog id
                backlog_id = self.db.get_backlog_id()
                if not backlog_id:
                    raise ValidationError("No backlog ID found to continue")
                
            logger.debug(f"Latest backlog ID retrieved: {backlog_id}")
            
            backlog_record = self.db.get_backlog_item(backlog_id)
            if not backlog_record:
                raise ValidationError(f"Backlog ID {backlog_id} not found")
            # logger.debug(f"Backlog record retrieved: {backlog_record}") 
            
            project_id = backlog_record['project_id']
            req_doc_id = backlog_record['requirement_doc_id']
            current_backlog = backlog_record['backlog_content']
            ## Get the iteration count from feedback history
            iteration_count = self.db.get_latest_feedback_iteration(backlog_id)
            
            # Review and refine backlog
            updated_items, iteration, all_feedback = await self.generate_feedback_mechanism(current_backlog, 
                                                    project_id, backlog_id,(int(iteration_count)+1) )
                    
            # Get final results
            final_backlog = updated_items if iteration > 0 else current_backlog
            product_backlog = final_backlog 
            
            logger.debug(f"Final Product Backlog after continuation: {product_backlog}")
            
            # # Return deliverables
            result = {
                'status': 'success',
                'product_backlog': product_backlog,
                'feedback_cycles': iteration,
                'total_feedback_items': len(all_feedback)
            }
            
            logger.info("Deliverables generated successfully")
            logger.debug(f"Deliverables Result: {result}")
            return result            
            
        except Exception as e:
            logger.error("Failed to continue backlog", exception=e)
            raise
    
    
    async def generate_deliverables(self, user_input: Dict[str, str]) -> Dict[str, Any]:
        """
        Generate requirement document and product backlog
        
        Args:
            user_input: Dictionary containing project details
        
        Returns:
            Dictionary containing both deliverables
        """
        try:
            logger.info("Starting deliverables generation process")
            
            project_name = user_input['project_name']
            project_description = user_input['description']
            user_requirements = user_input['user_requirements']
            tech_stack = user_input['tech_stack']
            
            # Create project in database
            project_id = self.db.create_project(project_name, project_description, user_requirements, str(tech_stack))            


            # Step 1: Generate detailed requirement document
            logger.info("Step 1: Generating requirement document...")
            response = await self.requirements_agent.create_requirements_document(
                project_id
            )

            requirements_doc = response['content']
            req_doc_id = response['req_doc_id']
            
            # Step 2: Generate product backlog from requirements
            logger.info("Step 2: Generating product backlog...")
            backlog_id, product_backlog = await self.backlog_agent.create_product_backlog(project_id, 
                                                                        req_doc_id, requirements_doc)
            
            # Step 3: Review and refine backlog
            updated_items, iteration, all_feedback = await self.generate_feedback_mechanism(product_backlog, 
                                                                                      project_id, backlog_id)
                    
            # Get final results
            final_backlog = updated_items if iteration > 0 else product_backlog
            product_backlog = final_backlog 
            
            logger.debug(f"Final Product Backlog: {product_backlog}")
            
            
            # # Return both deliverables
            result = {
                'status': 'success',
                'project_name': user_input['project_name'],
                'requirement_document': requirements_doc,
                'product_backlog': product_backlog,
                'feedback_cycles': iteration,
                'total_feedback_items': len(all_feedback)
            }
            
            logger.info("Deliverables generated successfully")
            logger.debug(f"Deliverables Result: {result}")
            return result
            
        except BaseAppException as e:
            logger.error("Deliverables generation failed", exception=e)
            return {
                'status': 'failed',
                'error': e.message
            }
        except Exception as e:
            logger.error("Unexpected error during deliverables generation", exception=e)
            return {
                'status': 'failed',
                'error': f'Unexpected system error: {str(e)}'
            }


def main():
    """Main function"""
    try:
        # Initialize orchestrator
        orchestrator = RequirementsOrchestrator()
        
        # Sample user input
        user_input = {
            'project_name': 'Automated Web Trading Platform',
            'description': '''A web-based trading application that automatically executes predefined trading strategies 
             using Zerodha API with real-time market data analysis and automated order execution.''',
            'user_requirements': """
            The system should provide:
            1. Secure Zerodha API integration with encrypted credential storage and OAuth2 authentication
            2. Real-time market data streaming for stocks, indices, and derivatives
            3. Strategy configuration interface for creating, testing, and deploying trading algorithms
            4. Automated order execution based on predefined strategy triggers and conditions
            5. Portfolio dashboard with live P&L, position tracking, and performance analytics
            6. Backtesting module to validate strategies against historical data
            7. Risk management features including position sizing, stop-loss, and exposure limits
            8. Trade journal with automated logging of all executions and strategy decisions
            9. Real-time alerts and notifications for strategy triggers and system events
            10. User management with role-based access control (admin, trader, viewer)
            """,
            'tech_stack': {
                'frontend': 'React with TypeScript, Chart.js/D3.js, WebSocket client',
                'backend': 'Python (FastAPI), Celery for async tasks, Redis for caching',
                'database': 'sqllite for user data, TimescaleDB for market data',
                'broker_integration': 'Zerodha Kite API, pykiteconnect SDK',
                'real_time_processing': 'WebSocket, Redis Pub/Sub, Kafka for event streaming',
                'infrastructure': 'Docker, AWS EC2/EKS, RDS, CloudWatch for monitoring',
                'authentication': 'JWT tokens, OAuth2, SSL encryption'
            },
            'key_features': [
                'Multi-strategy automation engine',
                'Real-time market data pipeline',
                'Paper trading mode for strategy testing',
                'Performance analytics and reporting',
                'API rate limit management and error handling',
                'Mobile-responsive web interface'
            ]
        }
        
        # Generate deliverables
        # logger.info("Starting functional requirements generation system")
        # result = asyncio.run(orchestrator.generate_deliverables(user_input))
        
        ### continue generating backlog from latest backlog id and from the latest feedback iteration
        logger.info("Continuing backlog generation from latest backlog ID")
        result = asyncio.run(orchestrator.continue_backlog_gen())
        
    except Exception as e:
        print(f"Critical error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()