"""Custom exception classes for the application."""


class ApplicationException(Exception):
    """Base exception class for the application."""

    def __init__(self, message: str, status_code: int = 500):
        """Initialize exception.

        Args:
            message: Exception message
            status_code: HTTP status code
        """
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class ValidationException(ApplicationException):
    """Raised when validation fails."""

    def __init__(self, message: str):
        """Initialize validation exception."""
        super().__init__(message, status_code=422)


class NotFoundException(ApplicationException):
    """Raised when a resource is not found."""

    def __init__(self, message: str = "Resource not found"):
        """Initialize not found exception."""
        super().__init__(message, status_code=404)


class AuthenticationException(ApplicationException):
    """Raised when authentication fails."""

    def __init__(self, message: str = "Authentication failed"):
        """Initialize authentication exception."""
        super().__init__(message, status_code=401)


class AuthorizationException(ApplicationException):
    """Raised when authorization fails."""

    def __init__(self, message: str = "Insufficient permissions"):
        """Initialize authorization exception."""
        super().__init__(message, status_code=403)
