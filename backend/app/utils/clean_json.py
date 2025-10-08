import re
import json
from utils import get_logger

logger = get_logger(__name__)


def clean_markdown_json(json_string):
    """
    Remove Markdown code block markers from JSON string
    Handles various formats:
    - ```json { ... } ```
    - ``` { ... } ```
    - ~~~json { ... } ~~~
    - And other variants
    """
    if not isinstance(json_string, str):
        return json_string
    
    # Remove ```json and ``` markers (with optional language specification)
    # Handles: ```json, ```JSON, ```, ~~~json, ~~~
    cleaned = re.sub(r'^```\w*\s*', '', json_string, flags=re.MULTILINE | re.IGNORECASE)
    cleaned = re.sub(r'^~~~\w*\s*', '', cleaned, flags=re.MULTILINE | re.IGNORECASE)
    cleaned = re.sub(r'\s*```\s*$', '', cleaned, flags=re.MULTILINE | re.IGNORECASE)
    cleaned = re.sub(r'\s*~~~\s*$', '', cleaned, flags=re.MULTILINE | re.IGNORECASE)
    
    # Also handle cases where markers might be on the same line as JSON
    cleaned = re.sub(r'^```\w*\s*\{', '{', cleaned, flags=re.MULTILINE | re.IGNORECASE)
    cleaned = re.sub(r'^~~~\w*\s*\{', '{', cleaned, flags=re.MULTILINE | re.IGNORECASE)
    cleaned = re.sub(r'\}\s*```\s*$', '}', cleaned, flags=re.MULTILINE | re.IGNORECASE)
    cleaned = re.sub(r'\}\s*~~~\s*$', '}', cleaned, flags=re.MULTILINE | re.IGNORECASE)
    
    return cleaned.strip()

def progressive_json_repair(json_string):

    # Strategy 0: Clean Markdown first
    def clean_markdown(s):
        return clean_markdown_json(s)

    """Try multiple repair strategies with increasing aggressiveness"""
    strategies = [
        clean_markdown,
        
        # Strategy 1: Basic comma fixes
        lambda s: re.sub(r'"\s*\n\s*"', '",\n"', s),
        
        # Strategy 2: Same-line comma fixes  
        lambda s: re.sub(r'"\s*"\s*"', '","', s),
        
        # Strategy 3: Remove trailing commas
        lambda s: re.sub(r',\s*\]', ']', re.sub(r',\s*\}', '}', s)),
        
        # Strategy 4: Add missing commas before objects/arrays
        lambda s: re.sub(r'"\s*\{', '", {', re.sub(r'"\s*\[', '", [', s)),
    ]
    
    current_string = json_string
    
    for i, strategy in enumerate(strategies):
        try:
            current_string = strategy(current_string)
            parsed = json.loads(current_string)
            logger.info(f"✅ Repaired with strategy {i + 1}")
            return parsed
        except json.JSONDecodeError as e:
            logger.error(f"❌ Strategy {i + 1} failed: {e}")
            continue