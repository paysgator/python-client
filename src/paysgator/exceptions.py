class PaysgatorError(Exception):
    """Base exception for Paysgator SDK"""
    def __init__(self, message: str = "", endpoint=None, method=None, response_body=None):
        self.endpoint = endpoint
        self.method = method
        self.response_body = response_body
        super().__init__(message)

class AuthenticationError(PaysgatorError):
    """Raised when authentication fails"""
    pass

class APIError(PaysgatorError):
    """Raised when the API returns an error"""
    def __init__(self, status_code: int, message: str, endpoint=None, method=None, response_body=None):
        self.status_code = status_code
        self.message = message
        super().__init__(f"API Error {status_code}: {message}", endpoint, method, response_body)
