from fastapi import HTTPException, status
class AppException(HTTPException):
    """base exception for all application errors.
    rvery custom exception inherits from this so we can catch
    appException globally in one place if needed."""
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)
class NotFoundException(AppException):
    def __init__(self, resource: str = "Resource"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} not found.",
        )
class UnauthorizedException(AppException):
    def __init__(self, detail: str = "Not authenticated."):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
        )
class ForbiddenException(AppException):
    def __init__(self, detail: str = "You do not have access to this resource."):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,)
class ConflictException(AppException):
    def __init__(self, detail: str = "Resource already exists."):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,)
class BadRequestException(AppException):
    def __init__(self, detail: str = "Bad request."):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,)
class LLMException(AppException):
    """Raised when the LLM provider returns an error."""
    def __init__(self, detail: str = "LLM provider error."):
        super().__init__(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=detail,)