# llm/ai_models.py
from abc import ABC, abstractmethod
from time import sleep, time
from typing import Dict, Any, Optional
from enum import Enum
from openai import OpenAI
from utils import get_logger


import openai
from utils import LLMError, AuthenticationError, apikeyError
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


logger = get_logger(__name__)


class AIModel(ABC):
    @abstractmethod
    def invoke(self, prompt: str) -> str:
        pass


class OpenAIModel(AIModel):
    def __init__(self, api_key: str, llm_model: str, base_url: Optional[str] = None):
        self.model = OpenAI(api_key=api_key)
        self.llm_model = llm_model
        self.base_url = base_url
        logger.debug(f"self.api_key : {api_key}")
        logger.debug(f"self.llm_model : {self.llm_model}")
        logger.debug(f"self.base_url : {self.base_url}")
                               

    def invoke(self, prompt: str, max_retries: int = 3) -> str:
        logger.debug("Invoking OpenAI API")

        try:
            response = self.model.chat.completions.create(
                model = self.llm_model,
                messages = [
                    {"role": "system", "content": "You are an experience agile product manager \
                     who is an expert in writing user stories, acceptance criteria, and test cases."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,  # Controls creativity (0 = deterministic, 1 = creative)
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            # logger.debug(f"response : {response}")
            return response.choices[0].message.content.strip()
        except openai.AuthenticationError as e:
            logger.error("Authentication error with OpenAI API", exception=e)
            raise
        except openai.error.RateLimitError as e:
            logger.error("Rate limit exceeded when calling OpenAI API", exception=e)
            raise LLMError("Rate limit exceeded. Please try again later.")
        except openai.error.OpenAIError as e:
            logger.error("OpenAI API error", exception=e)
            raise LLMError(f"OpenAI API error: {e}")
        except Exception as e:
            logger.error(f"Error calling OpenAI LLM: {e}")
            return f"Sorry, I couldn't generate a response. Please try again. {e}"

    
class HuggingFaceModel(AIModel):
    def __init__(self, model_name: str):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True, torch_dtype=torch.bfloat16)

    def invoke(self, prompt: str, max_retries: int = 3) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(**inputs)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    
    
class DeepSeekModel(AIModel):
    def __init__(self, api_key: str,  llm_model: str, base_url: Optional[str] = None):       
        self.api_key = api_key
        self.llm_model = llm_model
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
            # logger.debug("response-------------------------------- : ", response.choices[0].message.content)
            # Extract and return the generated text
            logger.debug(f"response === {response}")
            return response.choices[0].message.content.strip()

        except Exception as e:
            # Handle errors gracefully
            logger.error(f"Error calling LLM: {e}")
            return {"error_status_900" : f"Error occurred {e}"}
    
    
class PerplexityModel(AIModel):
    def __init__(self, api_key: str,  llm_model: str, base_url: Optional[str] = None):       
        self.api_key = api_key
        self.llm_model = llm_model
        self.base_url = base_url
        # logger.debug(f"self.api_key : {self.api_key}")
        logger.debug(f"self.llm_model : {self.llm_model}")
        logger.debug(f"self.base_url : {self.base_url}")  


    def invoke(self, prompt: str, max_retries: int = 3) -> str:
        logger.debug("Invoking Perplexity API")
        last_exception = None
        for attempt in range(max_retries + 1):
            try:
                logger.debug(f"Attempt {attempt + 1}: Invoking {self.llm_model} API")
                # Call the Perplexity API
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
                # logger.debug("response-------------------------------- : ", response.choices[0].message.content)
                # Extract and return the generated text
                return response.choices[0].message.content.strip()

            except openai.AuthenticationError as e:
                logger.error("Authentication error with Perplexity API", exception=e)
                raise
            
            except Exception as e:
                # Handle errors gracefully
                last_exception = e
                logger.error(f"Error calling LLM on attempt {attempt + 1}: {e}")               
                if attempt < max_retries:
                    delay = min(2 ** attempt, 10)  # Exponential backoff, max 10 seconds
                    logger.warning(f"Attempt {attempt + 1} failed. Retrying in {delay}s.")
                    sleep(delay)
                else:
                    logger.error(f"All {max_retries} attempts failed")
                    raise last_exception

                # return f"Sorry, I couldn't generate a response. Please try again. {e}"
    
class AIAdapter:
    def __init__(self, configs: dict, model_type: str):
        logger.debug(f"model type in AIAdapter : {model_type}")
        self.model = self._create_model(configs, model_type)

    def _create_model(self, configs: dict, model_type : str) -> AIModel:
        logger.debug(f"model type in create model of AIAdapter : {model_type}")
        logger.debug(f"configs in create model of AIAdapter : {configs}")
        for config in configs:
            logger.debug(f"config in create model of AIAdapter : {config}")
            if model_type in config.get("name"):
                llm_model = config['model_name']
                logger.debug(f"llm_model : {llm_model}")
                llm_api_key = config['api_key']
                base_url = config.get("base_url", "")
                # logger.debug(f"llm_api_key : {llm_api_key}")
                logger.debug(f"Using {model_type} with {llm_model}")
                break
            

            
        if model_type == "openai":
            return OpenAIModel(api_key=llm_api_key, llm_model=llm_model, base_url=base_url)
        elif model_type == "deepseek":
            return DeepSeekModel(api_key=llm_api_key, llm_model=llm_model, base_url=base_url)
        elif model_type == "perplexity":
            return PerplexityModel(api_key=llm_api_key, llm_model=llm_model, base_url=base_url)   
        elif model_type == "huggingface":
            return HuggingFaceModel(model_name=llm_model)
        else:    
            raise ValueError(f"Unsupported model type: {model_type}")
        
        
    def invoke(self, prompt: str) -> str:
        return self.model.invoke(prompt)
