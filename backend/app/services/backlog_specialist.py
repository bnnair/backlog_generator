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
            
#             prompt = f"""
# Convert the following requirements document into a detailed product backlog with user stories and acceptance criteria:

# REQUIREMENTS DOCUMENT:
# {requirements_doc}

# Please create a comprehensive product backlog with the following structure for each item:

# - EPIC: High-level feature or theme
# - TITLE: Brief, descriptive title
# - DESCRIPTION: Detailed description of the feature
# - USER STORY: In the format "As a [user], I want to [action], so that [benefit]"
# - ACCEPTANCE CRITERIA: Clear, testable criteria (bulleted list)
# - PRIORITY: must have, should have, could have, won't have (MoSCoW)
# - ESTIMATE: Story points or T-shirt sizes (S/M/L/XL)
# - DEPENDS_ON: List any dependencies on other backlog items

# The stories should be clear, concise, and actionable with quantitative acceptance criteria. Each story should be independent 
# and valuable as well as testable on its own. 

# Organize the backlog by functional areas and ensure proper prioritization. no extra text outside the document structure included.
# """
     
            prompt = f"""
            Convert the following requirements document into a detailed product backlog with user stories and acceptance criteria.
Ensure both technical and business aspects are fulfilled in the user stories.
REQUIREMENTS DOCUMENT:
{requirements_doc}

Create a comprehensive product backlog with the following standard JSON structure:
example:
{{
  "product_backlog": {{
    "project_name": "Customer Management System",
    "version": "1.0",
    "created_date": "2024-01-15",
    "epics": [
      {{
        "epic_name": "Customer Profile Management",
        "user_stories": [
          {{
            "story_id": "US-1",
            "title": "Brief, descriptive title",
            "description": "Detailed description of the feature",
            "user_story": "As a [user], I want to [action], so that [benefit]",
            "acceptance_criteria": [
              "Clear, testable criteria 1",
              "Clear, testable criteria 2"
            ],
            "priority": "must have",
            "estimate": "M",
            "depends_on": [],
            "definition_of_done": [
              "All acceptance criteria are met",
              "Code is reviewed and tested",
              "Documentation is updated"
            ]
          }}
        ]
      }}
    ]
  }}
}}

Requirements:
- Each story should be clear, concise, and actionable
- Acceptance criteria should be quantitative and testable
- Stories should be independent and valuable.
- Stories related to performance testing, mobile, batch jobs, offline criteria, audit logs, localization, 
  multi-language, third party integration, infrastructure,  accessability, etc must be avoided.
- Organize by functional areas with proper prioritization
- Use MoSCoW prioritization method
- Use T-shirt sizing for estimates (S/M/L/XL)
- No extra text outside the JSON structure. No backticks or extra text before the JSON structure.
"""
            
            response = self.llm_adapter.invoke(
                prompt)
            
            if "error_status_900" in response:
              logger.error(f"Error happened during creatingcreation of product backlog by llm: {response} ")
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
    
    async def improve_backlog(self, backlog_content: str, feedback: str) -> str:
        """Improve backlog based on feedback"""
        try:
            logger.info("Improving backlog based on feedback")
            
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
- Stories related to performance testing, mobile, batch jobs, offline criteria, audit logs, localization, 
  multi-language, third party integration, infrastructure,  accessibility, etc must be avoided.
- Please update the backlog to address the feedback while maintaining proper structure and clarity. 
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