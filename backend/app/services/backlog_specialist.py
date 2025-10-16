# agents/backlog_specialist.py
import json
from typing import Dict, Any, List
from services.llm_manager import AIAdapter
from utils.logger import get_logger
from utils.exceptions import ValidationError
from models.database import RequirementsDatabase

logger = get_logger(__name__)

class BacklogSpecialist:
    """Specialized agent for creating detailed product backlogs"""
    
    def __init__(self, llm_adapter: AIAdapter, agent_id: str, db: RequirementsDatabase):
        self.db = db
        self.agent_id = agent_id
        self.backlog_id=0   
        self.llm_adapter = llm_adapter
    
    async def create_product_backlog(self, project_id: int, req_doc_id: int,  requirements_doc: str) -> str:
        """Create a detailed product backlog from requirements document"""
        try:
            
            project = self.db.get_project(project_id)
            if not project:
                return []
            
            logger.info("Creating product backlog from requirements")
            
            # prompt = f"""
            # Convert the following requirements document into a detailed Functional product backlog with user stories 
            # and acceptance criteria. 
            # Ensure both technical and business aspects are fulfilled in the user stories.
            # REQUIREMENTS DOCUMENT:
            # {requirements_doc}

            # Create a comprehensive product backlog with the following standard JSON structure:
            # example:
            # {{
            #   "product_backlog": {{
            #     "project_name": "Customer Management System",
            #     "version": "1.0",
            #     "created_date": "2024-01-15",
            #     "epics": [
            #       {{
            #         "epic_name": "Customer Profile Management",
            #         "user_stories": [
            #           {{
            #             "story_id": "US-1",
            #             "title": "Brief, descriptive title",
            #             "description": "Detailed description of the feature",
            #             "user_story": "As a [user], I want to [action], so that [benefit]",
            #             "acceptance_criteria": [
            #               "Clear, testable criteria 1",
            #               "Clear, testable criteria 2"
            #             ],
            #             "priority": "must have",
            #             "estimate": "M",
            #             "depends_on": [],
            #             "definition_of_done": [
            #               "All acceptance criteria are met",
            #               "Code is reviewed and tested",
            #               "Documentation is updated"
            #             ]
            #           }}
            #         ]
            #       }}
            #     ]
            #   }}
            # }}

            # Requirements:
            # - Each story should be clear, concise, and actionable
            # - The backlog should contain only functional requirements. No NFR should
            #   be included.
            # - Acceptance criteria should be quantitative and testable
            # - Stories should be independent and valuable.
            # - Stories related to Non Functional requirements like performance testing, mobile, batch jobs, offline criteria, 
            #   audit logs, localization, multi-language, third party integration, infrastructure,  accessability, etc 
            #   must be strictly avoided.
            # - Organize by functional areas with proper prioritization
            # - Use MoSCoW prioritization method
            # - Use T-shirt sizing for estimates (S/M/L/XL)
            # - No extra text outside the JSON structure. No backticks or extra text before the JSON structure.
            # """
            
            prompt = f"""
            You are an expert product manager tasked with converting business requirements into a structured functional 
            product backlog. Your output must be exclusively valid JSON with no additional text, explanations, or markdown 
            formatting.

            **INPUT DOCUMENT:**
            {requirements_doc}

            **TASK:**
            Transform the provided requirements document into a detailed functional product backlog organized by epics, 
            containing user stories with comprehensive acceptance criteria.

            **REQUIREMENTS:**
            - Include ONLY functional requirements - strictly exclude all non-functional requirements
            - Each user story must follow the standard format: "As a [role], I want to [action], so that [benefit]"
            - Acceptance criteria must be quantitative, testable, and verifiable
            - Stories should be independent, valuable, and actionable
            - Organize stories into logical functional epics
            - Apply MoSCoW prioritization (must have/should have/could have/won't have)
            - Use T-shirt sizing for estimates (S/M/L/XL)

            **STRICTLY EXCLUDE:**
            Performance requirements, mobile-specific features, batch jobs, offline capabilities, audit logging, localization,
            multi-language support, third-party integrations, infrastructure concerns, accessibility features, and any other
            non-functional requirements.

            **OUTPUT FORMAT:**
            Your output must be valid JSON matching this exact structure:
            {{
              "product_backlog": {{
                "project_name": "string",
                "version": "string", 
                "created_date": "YYYY-MM-DD",
                "epics": [
                  {{
                    "epic_name": "string",
                    "user_stories": [
                      {{
                        "story_id": "string",
                        "title": "string",
                        "description": "string",
                        "user_story": "As a [role], I want to [action], so that [benefit]",
                        "acceptance_criteria": ["string"],
                        "priority": "must have|should have|could have|won't have",
                        "estimate": "S|M|L|XL",
                        "depends_on": ["story_id"],
                        "definition_of_done": ["string"]
                      }}
                    ]
                  }}
                ]
              }}
            }}
            """
            
            response = self.llm_adapter.invoke(
                prompt)
            
            if "error_status_900" in response:
              logger.error(f"Error happened during creation of product backlog by llm: {response} ")
              raise Exception(response)
            
            product_backlog = response
            logger.info("Product backlog created successfully")
            logger.debug(f"Generated Product Backlog: {product_backlog}")
            
            # Save backlog document to database
            backlog_id = self.db.add_backlog_item(project_id, req_doc_id, product_backlog, self.agent_id)
            self.backlog_id = backlog_id
            logger.debug("Backlog item saved to database with ID: {backlog_id} ")
            
            return backlog_id, product_backlog
            
        except Exception as e:
            logger.error("Failed to create product backlog", exception=e)
            raise
    
    async def improve_fr_backlog(self, backlog_content: str, feedback: str) -> str:
        """Improve backlog based on feedback"""
        try:
            logger.info("Improving backlog -FR based on feedback")
            
            # prompt = f"""
            # Improve the following product backlog based on the provided feedback to ensure that technical as well as 
            # business aspects are fulfilled. 
            # Ensure that the backlog JSON structure is kept as is while generating the updated backlog.
            # The feedback in the form of json structure is passed and each suggestion should be addressed in the improved backlog. first check if the 
            # suggestion is already addressed in the backlog, if yes then ignore it, otherwise incorporate the suggestion.
            # after incorporating the suggestion, if a story becomes bigger than size L, then break it down into smaller 
            # stories. Make sure dependencies are updated accordingly. Ensure the final backlog maintains clarity, 
            # proper structure, and prioritization.

            # ORIGINAL BACKLOG:
            # {backlog_content}

            # FEEDBACK TO INCORPORATE:
            # {feedback}
            # - Stories related to Non Functional requirements like performance testing, mobile, batch jobs, offline criteria, 
            #   audit logs, localization,multi-language, third party integration, infrastructure,  accessibility, etc 
            #   must be strictly avoided.
            # - Please update the backlog to address the appropriate feedback (only Functional requirement) while 
            #   maintaining proper structure and clarity. 
            # - no extra text outside the document structure included.  
            # - Strictly No "```json" or "```" or "json" in the response.
            # """

            prompt = f"""
            You are a product backlog manager updating a backlog based on specific feedback. 

            **ORIGINAL BACKLOG:**
            {backlog_content}

            **FEEDBACK TO INCORPORATE:**
            {feedback}

            **UPDATE RULES:**
            1. Process each feedback item in order
            2. For "update" actions: Modify the specified story field with the suggested change
            3. For "split" actions: Break the story into the specified number of smaller stories (2-3 stories max)
            4. For "add" actions: Create new story in the specified epic with appropriate details
            5. Update story IDs sequentially after any changes
            6. Maintain all original JSON structure and fields

            **OUTPUT REQUIREMENTS:**
            - Output ONLY the complete updated backlog as valid JSON
            - No explanations, no additional text
            - Preserve all original fields and structure
            - Ensure no markdown or code blocks

            **VALIDATION:**
            - All stories must have complete required fields
            - No story larger than size "L"
            - All dependencies must reference valid story IDs
            """
            
            response = self.llm_adapter.invoke(
                prompt)
            if "error_status_900" in response:
              logger.error(f"Error happened during improving backlog by llm: {response} ")
              raise Exception(response)

            improved_backlog = response
            logger.info("Backlog improved successfully")
            return improved_backlog
            
        except Exception as e:
            logger.error("Failed to improve backlog", exception=e)
            raise


    async def create_nfr_backlog(self, backlog_content: str) -> str:
        """Create NFR backlog based on feedback"""
        try:
            logger.info("Adding backlog - NFR ")
            
            prompt = f"""
            BACKLOG:
            {backlog_content}

            Based on the above product backlog, identify and generate comprehensive Non-Functional Requirements (NFRs) 
            as epics and user stories. Focus on:

            1. Performance & Scalability
            2. Security & Compliance
            3. Reliability & Availability
            4. Maintainability & Supportability
            5. Usability & Accessibility
            6. Compatibility & Integration

            Output Format: It should be similar to the backlog json structure. 
            - if any epic or user story becomes large, then split it into independant user stories.
            - no extra text outside the document structure included.  
            - Strictly No "```json" or "```" or "json" in the response.
            """
            
            response = self.llm_adapter.invoke(
                prompt)
            if "error_status_900" in response:
              logger.error(f"Error happened during improving backlog by llm: {response} ")
              raise Exception(response)

            improved_backlog = response
            logger.info("Backlog improved successfully")
            return improved_backlog
            
        except Exception as e:
            logger.error("Failed to improve backlog", exception=e)
            raise


    async def improve_nfr_backlog(self, backlog_content: str, feedback: str) -> str:
        """Update NFR backlog based on feedback"""
        try:
            logger.info("Updating backlog - NFR based on feedback")
            
            prompt = f"""
            Improve the following product backlog based on the provided feedback to ensure that technical as well as 
            business aspects are fulfilled:
            A json structure is passed and each suggestion should be addressed in the improved backlog. first check if the 
            suggestion is already addressed in the backlog, if yes then ignore it, otherwise incorporate the suggestion.
            after incorporating the suggestion, if a story becomes bigger than size L, then break it down into smaller 
            stories. Make sure dependencies are updated accordingly. Ensure the final backlog maintains clarity, 
            proper structure, and prioritization.

            ORIGINAL BACKLOG:
            {backlog_content}

            FEEDBACK TO INCORPORATE:
            {feedback}
            - Stories related to Non Functional requirements only to be updated.
            - Please update the backlog to address the appropriate feedback (only Non Functional requirement) while 
              maintaining proper structure and clarity. 
            - no extra text outside the document structure included.  
            - Strictly No "```json" or "```" or "json" in the response.
            """
            
            response = self.llm_adapter.invoke(
                prompt)
            if "error_status_900" in response:
              logger.error(f"Error happened during improving backlog by llm: {response} ")
              raise Exception(response)

            improved_backlog = response
            logger.info("Backlog improved successfully")
            return improved_backlog
            
        except Exception as e:
            logger.error("Failed to improve backlog", exception=e)
            raise