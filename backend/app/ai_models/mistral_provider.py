from typing import Optional
from utils import get_logger
from time import time, sleep
import os

from openai import OpenAI


logger = get_logger(__name__)


class MistralModel():
    def __init__(self, api_key_string: str,  model_name: str, base_url: Optional[str] = None):       
        self.api_key = os.environ[api_key_string]
        self.llm_model = model_name
        self.base_url = base_url
        # logger.debug(f"self.api_key : {self.api_key}")
        logger.debug(f"self.llm_model : {self.llm_model}")
        logger.debug(f"self.base_url : {self.base_url}")  


    def invoke(self, prompt: str, max_retries: int = 3) -> str:
        logger.debug("Invoking DeepSeek API")
        try:
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
            logger.debug(f"response === {response}")

            return response.choices[0].message.content.strip()

        except Exception as e:
            # Handle errors gracefully
            logger.error(f"Error calling LLM: {e}")
            return {"error_status_900" : f"Error occurred {e}"}