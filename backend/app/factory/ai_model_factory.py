import os
import yaml
import json
import importlib
from typing import Dict, Any, List
from pathlib import Path

from utils import get_logger

logger = get_logger(__name__)

class AIModelFactory:
    _model_configs = None
    _provider_configs = None
    
    @classmethod
    def initialize(cls, config_path: str = None):
        """Initialize the factory with configuration"""
        config_path = os.path.join(Path(__file__).resolve().parent.parent,"config","models.yaml")
        
        cls._load_configurations(config_path)
    
    @classmethod
    def _load_configurations(cls, config_path: str):
        """Load model and provider configurations from file"""
        config_file = Path(config_path)
        
        if not config_file.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(config_file, 'r', encoding='utf-8') as f:
            if config_path.endswith('.yaml') or config_path.endswith('.yml'):
                config_data = yaml.safe_load(f)
            else:
                config_data = json.load(f)
        
        cls._model_configs = config_data.get('models', {})
        cls._provider_configs = config_data.get('providers', [])
        
        logger.info(f"Loaded configurations for {len(cls._model_configs)} model types")
    
    @classmethod
    def create_model(cls, model_type: str, provider_configs: List[Dict] = None) -> Any:
        """Create model instance with dynamic configuration"""
        if cls._model_configs is None:
            cls.initialize()
        
        # Use provided configs or fall back to loaded provider configs
        configs_to_use = provider_configs or cls._provider_configs
        
        # Find matching provider configuration
        provider_config = cls._find_provider_config(model_type, configs_to_use)
        if not provider_config:
            raise ValueError(f"No provider configuration found for: {model_type}")
        
        # Get model specification
        model_spec = cls._model_configs.get(model_type)
        if not model_spec:
            raise ValueError(f"Model type not supported: {model_type}")
        
        # Prepare constructor arguments
        constructor_args = cls._prepare_arguments(model_spec, provider_config)
        
        # Dynamically create instance
        return cls._instantiate_model(model_spec['class_path'], constructor_args)
    
    @classmethod
    def _find_provider_config(cls, model_type: str, configs: List[Dict]) -> Dict[str, Any]:
        """Find provider configuration for the specified model type"""
        for config in configs:
            if model_type in config.get("name", ""):
                logger.debug(f"Found config for {model_type}: {config.get('model_name')}")
                return config
        return None
    
    @classmethod
    def _prepare_arguments(cls, model_spec: Dict, provider_config: Dict) -> Dict[str, Any]:
        """Prepare constructor arguments by merging defaults, required, and optional params"""
        constructor_args = {}
        
        # Add default parameters
        default_params = model_spec.get('default_params', {})
        if not default_params == None:
            constructor_args.update(default_params)
        
        # Add required parameters (override defaults if present)
        required_params = model_spec.get('required_params', [])
        for param in required_params:
            if param in provider_config:
                # Handle environment variable substitution
                value = cls._resolve_env_vars(provider_config[param])
                constructor_args[param] = value
            else:
                raise ValueError(f"Required parameter '{param}' missing from provider config")
        
        # Add optional parameters
        optional_params = model_spec.get('optional_params', [])
        for param in optional_params:
            if param in provider_config and param not in constructor_args:
                value = cls._resolve_env_vars(provider_config[param])
                constructor_args[param] = value
        
        return constructor_args
    
    @classmethod
    def _resolve_env_vars(cls, value: Any) -> Any:
        """Resolve environment variables in configuration values"""
        if isinstance(value, str) and value.startswith('${') and value.endswith('}'):
            env_var = value[2:-1]
            return os.getenv(env_var, value)
        return value
    
    @classmethod
    def _instantiate_model(cls, class_path: str, constructor_args: Dict) -> Any:
        """Dynamically import and instantiate the model class"""
        try:
            module_path, class_name = class_path.rsplit('.', 1)
            module = importlib.import_module(module_path)
            model_class = getattr(module, class_name)
            
            logger.info(f"Instantiating {class_name} with args: {list(constructor_args.keys())}")
            return model_class(**constructor_args)
            
        except (ImportError, AttributeError, ValueError) as e:
            logger.error(f"Failed to instantiate model {class_path}: {e}")
            raise
    
    @classmethod
    def get_available_models(cls) -> List[str]:
        """Get list of available model types"""
        if cls._model_configs is None:
            cls.initialize()
        return list(cls._model_configs.keys())
    
    @classmethod
    def get_model_config(cls, model_type: str) -> Dict[str, Any]:
        """Get configuration for a specific model type"""
        if cls._model_configs is None:
            cls.initialize()
        return cls._model_configs.get(model_type, {})
    
