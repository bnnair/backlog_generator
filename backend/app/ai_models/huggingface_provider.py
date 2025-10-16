
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from utils import get_logger


logger = get_logger(__name__)


class HuggingFaceModel():
    def __init__(self, model_name: str):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True, dtype=torch.bfloat16)
        logger.info(f"Hugging Face Model {model_name} initialized.")

    def invoke(self, prompt: str, max_retries: int = 3) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(**inputs)
        logger.debug(f"ouput ------ {outputs}")
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)