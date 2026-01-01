class PaysgatorError(Exception):
    """Base exception for Paysgator SDK"""
    pass

class AuthenticationError(PaysgatorError):
    """Raised when authentication fails"""
    pass

class APIError(PaysgatorError):
    """Raised when the API returns an error"""
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"API Error {status_code}: {message}")
