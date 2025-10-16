# agents/requirements_specialist.py
from typing import Dict, Any
from services.llm_manager import AIAdapter
from utils.logger import get_logger
from models.database import RequirementsDatabase


logger = get_logger(__name__)

class RequirementsSpecialist:
    """Specialized agent for creating detailed requirement documents"""
    
    def __init__(self, llm_adapter: AIAdapter, agent_id: str, db: RequirementsDatabase):
        self.db = db
        self.agent_id = agent_id
        self.req_doc_id = 0
        self.llm_adapter = llm_adapter
    
    async def create_requirements_document(self, project_id: int) -> str:
        """Create a comprehensive requirement document using LLM"""
        try:
            
            project = self.db.get_project(project_id)
            if not project:
                return "Project not found"            
            
            
            logger.info(f"Creating requirement document for: {project['name']}")
            
            prompt = f"""
            Create a detailed and professional software requirements document for the following project:

            PROJECT NAME: {project['name']}
            TECHNOLOGY STACK: {project['tech_stack']}
            USER REQUIREMENTS: {project['user_requirements']}

            Please structure the document with the following sections:

            1. PROJECT OVERVIEW
            - Project Description
            - Objectives and Goals
            - Scope and Boundaries

            2. BUSINESS REQUIREMENTS
            - Business Objectives
            - Success Criteria
            - Key Performance Indicators

            3. FUNCTIONAL REQUIREMENTS
            - System Features and Capabilities
            - User Stories (high-level)
            - Data Management Requirements

            4. NON-FUNCTIONAL REQUIREMENTS
            - Performance Requirements
            - Security Requirements
            - Usability Requirements
            - Reliability and Availability

            5. TECHNICAL SPECIFICATIONS
            - Architecture Overview
            - Technology Stack Details
            - Integration Requirements

            6. CONSTRAINTS AND ASSUMPTIONS
            - Technical Constraints
            - Business Constraints
            - Key Assumptions

            Ensure the document is comprehensive, well-structured, and suitable for development teams. 
            Also ensure no extra text outside the document structure included. 
            """
            
            response = self.llm_adapter.invoke(
                prompt)
            
            if "error_status_900" in response:
                logger.error(f"Error occurred during requirement document generation by llm : {response}")
                raise Exception(response)

            requirements_doc = response
            logger.info("Requirement document created successfully:")
            logger.debug(f"Requirement Document: {requirements_doc}")
            
            # Save requirements document to database
            doc_id = self.db.save_requirement_document(project_id, requirements_doc, self.agent_id)
            self.req_doc_id = doc_id
            response = {"req_doc_id": doc_id, "content": requirements_doc}
            return response
            
        except Exception as e:
            logger.error("Failed to create requirement document", exception=e)
            raise

    async def review_fr_backlog(self, backlog_content: str, project_id: int, backlog_id: int, feedback_id: int) -> str:
        """Review product backlog for completeness and quality"""
        try:
            logger.info("Reviewing product backlog")
            
            # prompt = f"""
            # Review the following product backlog which is in json format and provide specific feedback on:

            # 1. Completeness - Are all requirements covered?
            # 2. Clarity - Are user stories and acceptance criteria clear?
            # 3. Prioritization - Is the backlog properly prioritized?
            # 4. Technical feasibility - Are the items technically achievable?

            # PRODUCT BACKLOG:
            # {backlog_content}

            # The structure should be the json structure below..
            # {{
            #     "feedback": {{
            #         "completeness": {{
            #             "suggestions": [
            #                 "suggestion 1",
            #                 "suggestion 2",
            #                 "suggestion 3"
            #             ],
            #         }},
            #         "clarity": {{
            #             "suggestions": [
            #                 "suggestion 1",
            #                 "suggestion 2"
            #             ],
            #         }},
            #         "Prioritization": {{
            #             "suggestions": [
            #                 "suggestion 1",
            #                 "suggestion 2"
            #             ],
            #         }},
            #         "Technical feasibility": {{
            #             "suggestions": [
            #                 "suggestion 1",
            #                 "suggestion 2"
            #             ],
            #         }}
            #     }},   
            # }}
            # 1. Provide feedback only on Functional Requirement. NFR or Non Functional requirement feedback should be strictly
            # avoided.
            # 2. Provide constructive feedback with specific suggestions for improvement related to Functional requirement 
            # only in Json format. Do not provide any trivial feedback.
            # 3. feedback on Stories related to Non Functional requirement like performance testing, mobile, batch jobs, 
            # offline criteria, audit logs, localization, multi-language, third party integration, infrastructure,  
            # accessability, etc must be strictly avoided.
            # 4. If no feedback, then return None.  no extra text outside the document structure included. 
            # 5. The suggestion arrays can have multiple suggestions. Above shown is just an example with 2 or 3 items. 

            # Before finalizing, validate that:
            # 1. All arrays have commas between items
            # 2. No trailing commas after last array items  
            # 3. All strings are properly quoted
            # 4. All brackets and braces are properly closed
            # 5. Strictly No "```json" or "```" or "json" in the response.
            # """
            
            prompt = f'''
            You are an experienced product owner reviewing a product backlog. Provide actionable, specific feedback 
            that can be easily implemented.

            PRODUCT BACKLOG:
            {backlog_content}

            FEEDBACK STRUCTURE:
            {{
            "feedback": {{
                "required_changes": [
                {{
                    "action": "update",
                    "story_id": "US-1",
                    "field": "acceptance_criteria",
                    "change": "Add validation for email format",
                }},
                {{
                    "action": "split", 
                    "story_id": "US-3",
                    "reason": "Story too large (XL)",
                    "new_stories": 2
                }},
                {{
                    "action": "add",
                    "epic": "Customer Management",
                    "story_description": "Delete customer functionality"
                }},
                {{...
                }},
                ]
            }}
            }}
            **GUIDELINES:**
            - Focus ONLY on functional requirements
            - Be specific and actionable - avoid vague feedback
            - For story splits, provide clear breakdown of suggested new stories
            - Include story IDs for traceability
            - If no feedback in a category, use empty array []
            - No non-functional requirement feedback

            **OUTPUT:** Only valid JSON following above structure
            '''
            
            response = self.llm_adapter.invoke(
                prompt)
                        
            if "error_status_900" in response:
                logger.error(f"Error occurred during reviewing the backlog by llm : {response}")
                raise Exception(response)
            
            feedback = response
            logger.info("Backlog review completed")
            logger.debug(f"Backlog Feedback: {feedback}")
            
            feedback_id = self.db.add_review_feedback(feedback_id, project_id, backlog_id, feedback, "Action required", self.agent_id)
            
            return feedback
            
        except Exception as e:
            logger.error("Failed to review backlog", exception=e)
            raise
        
        
    async def review_nfr_backlog(self, backlog_content: str, project_id: int, backlog_id: int, feedback_id: int) -> str:
        """Review product backlog for completeness and quality"""
        try:
            logger.info("Reviewing product backlog")
            
            prompt = f"""
            Review the following product backlog which is in json format and provide specific feedback on:

            1. Completeness - Are all requirements covered?
            2. Clarity - Are user stories and acceptance criteria clear?
            3. Prioritization - Is the backlog properly prioritized?
            4. Technical feasibility - Are the items technically achievable?

            PRODUCT BACKLOG:
            {backlog_content}

            The structure should be the json structure below..
            {{
                "feedback": {{
                    "completeness": {{
                        "suggestions": [
                            "suggestion 1",
                            "suggestion 2",
                            "suggestion 3"
                        ],
                    }},
                    "clarity": {{
                        "suggestions": [
                            "suggestion 1",
                            "suggestion 2"
                        ],
                    }},
                    "Prioritization": {{
                        "suggestions": [
                            "suggestion 1",
                            "suggestion 2"
                        ],
                    }},
                    "Technical feasibility": {{
                        "suggestions": [
                            "suggestion 1",
                            "suggestion 2"
                        ],
                    }}
                }},   
            }}
            1. Provide feedback only on Functional Requirement. NFR or Non Functional requirement feedback should be strictly
            avoided.
            2. Provide constructive feedback with specific suggestions for improvement related to Functional requirement 
            only in Json format. Do not provide any trivial feedback.
            3. feedback on Stories related to Non Functional requirement like performance testing, mobile, batch jobs, 
            offline criteria, audit logs, localization, multi-language, third party integration, infrastructure,  
            accessability, etc must be strictly avoided.
            4. If no feedback, then return None.  no extra text outside the document structure included. 
            5. The suggestion arrays can have multiple suggestions. Above shown is just an example with 2 or 3 items. 

            Before finalizing, validate that:
            1. All arrays have commas between items
            2. No trailing commas after last array items  
            3. All strings are properly quoted
            4. All brackets and braces are properly closed
            5. Strictly No "```json" or "```" or "json" in the response.
            """
            
            response = self.llm_adapter.invoke(
                prompt)
                        
            if "error_status_900" in response:
                logger.error(f"Error occurred during reviewing the backlog by llm : {response}")
                raise Exception(response)
            
            feedback = response
            logger.info("Backlog review completed")
            logger.debug(f"Backlog Feedback: {feedback}")
            
            feedback_id = self.db.add_review_feedback(feedback_id, project_id, backlog_id, feedback, "Action required", self.agent_id)
            
            return feedback
            
        except Exception as e:
            logger.error("Failed to review backlog", exception=e)
            raise