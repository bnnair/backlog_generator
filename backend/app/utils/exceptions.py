

# utils/exceptions.py

class BaseAppException(Exception):
    """Base exception for the application"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class LLMError(BaseAppException):
    """LLM API and processing errors"""
    pass

class ValidationError(BaseAppException):
    """Data validation errors"""
    pass

class AuthenticationError(BaseAppException):
    """Authentication related errors"""
    pass

class apikeyError(BaseAppException):
    """API key related errors"""
    pass