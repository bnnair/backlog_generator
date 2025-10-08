# utils/logger.py
import logging
import sys
from pathlib import Path
from typing import Dict, Any

def get_logger(name: str):
    """Get a configured logger instance"""
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        # Create logs directory
        parent_folder = Path(__file__).parent.parent
        log_dir = Path.joinpath(parent_folder, "logs")
        print( f"log_dir : {log_dir}" )
        log_dir.mkdir(exist_ok=True)
        
        # Configure logging
        logger.setLevel(logging.DEBUG)
        
        # File handler
        file_handler = logging.FileHandler(log_dir / "requirements_generation.log", encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger