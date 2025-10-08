from pathlib import Path
from utils import get_logger
import yaml
import os

logger = get_logger(__name__)


class ConfigError(Exception):
    pass
11

class ConfigManager:
    
    @staticmethod
    def validate_yaml_file(yaml_path: Path) -> dict:
        try:
            with open(yaml_path, 'r') as stream:
                return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            raise ConfigError(f"Error reading file {yaml_path}: {exc}")
        except FileNotFoundError:
            raise ConfigError(f"File not found: {yaml_path}")
        
    @staticmethod
    def update_config() -> tuple:
        secrets_file = Path(__file__).resolve().parent.parent / 'models' / 'data' / 'secrets.yaml'
        # logger.debug(f"secrets_file : {secrets_file}")
        
        if not secrets_file.exists():
            raise FileNotFoundError(
                f"Secrets file not found: {secrets_file}")

        secrets = ConfigManager.validate_yaml_file(secrets_file)
        config_list = []
        try:
            for v in secrets['llm_model_type']:
                config = {}
                # logger.debug(f" model types : {v}")
                config.update({"name" : v.get("name")})
                config.update({"model_name" : v.get("model_name")})
                api_str = v.get("api_key_string")
                if api_str == '':
                    api_key = ''
                else:
                    api_key = os.environ[api_str]
                # logger.debug(f"api_key : {api_key}")
                config.update({"api_key" : api_key})
                config.update({"base_url" : v.get("base_url")})
                config_list.append(config)
                # logger.debug(f"model_name : {model_name}")
                # logger.debug(f"api_key_string : {api_str}")    
            logger.debug(f"config :{config_list}")    
        except KeyError as e:
            raise ConfigError(f"Missing expected key in secrets file: {e}")

        return config_list
