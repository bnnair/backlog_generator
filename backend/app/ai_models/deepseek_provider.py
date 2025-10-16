import traceback
from typing import Optional
from utils import get_logger
from time import time, sleep
import os
import json

from openai import OpenAI


logger = get_logger(__name__)


class DeepSeekModel():
    def __init__(self, api_key_string: str,  model_name: str, base_url: Optional[str] = None):       
        self.api_key = os.environ[api_key_string]
        self.llm_model = model_name
        self.base_url = base_url
        # logger.debug(f"self.api_key : {self.api_key}")
        logger.debug(f"self.llm_model : {self.llm_model}")
        logger.debug(f"self.base_url : {self.base_url}")  


    def invoke(self, prompt: str, max_retries: int = 5) -> str:
        logger.debug("Invoking DeepSeek API")
        for attempt in range(max_retries):
            try:
                logger.info(f"Attempt {attempt + 1} to load model...")
                # Call the Deepseek API
                client = OpenAI(api_key=self.api_key, base_url=self.base_url) 
                logger.debug(f"client : {client}")
                logger.info(f"prompt-------: {prompt}")
                logger.info(f"llm model -----> {self.llm_model}")
                sleep(2)  # To avoid rate limiting issues
                response = client.chat.completions.create(
                    model=self.llm_model, 
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.8  # Controls creativity (0 = deterministic, 1 = creative)
                    # max_tokens=500,   # Limit the length of the response
                )
                # Extract and return the generated text
                # logger.debug(f"response === {response}")

                return response.choices[0].message.content.strip()

            except json.JSONDecodeError as e:
                # This is likely the actual exception you're getting
                logger.info(f"Error (attempt {attempt + 1}): {e}")
                
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 30  # Increasing wait time
                    logger.error(f"JSON decode error: {e}")
                    logger.error(f"Error at position {e.pos}, line {e.lineno}, column {e.colno}")
                    logger.info(f"Waiting {wait_time} seconds before retry...")
                    sleep(wait_time)
                else:
                    return {"error_status_900" : f"Error occurred {e}"}
            
            except Exception as e:
                # Get full traceback
                logger.error(f"Full error traceback:\n{traceback.format_exc()}")
                
                # Log the request details that might help debugging
                logger.error(f"Request details - model: {self.llm_model}, prompt length: {len(prompt)}")
                
                # If it's an API error, get more details
                if hasattr(e, 'response'):
                    logger.error(f"Response status: {e.response.status_code}")
                    logger.error(f"Response headers: {dict(e.response.headers)}")
                    try:
                        response_text = e.response.text
                        logger.error(f"Response text: {response_text}")
                    except:
                        logger.error("Could not read response text")
                
                # Re-raise or handle as appropriate
                return {"error_status_900" : f"Error occurred {e}"}