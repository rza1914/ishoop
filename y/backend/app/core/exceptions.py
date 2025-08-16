from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import logging

logger = logging.getLogger(__name__)

class BaseHTTPException(Exception):
    """Base HTTP exception class"""
    def __init__(self, status_code: int, message: str, detail: str = None):
        self.status_code = status_code
        self.message = message
        self.detail = detail

class ValidationException(BaseHTTPException):
    """Validation error exception"""
    def __init__(self, message: str, detail: str = None):
        super().__init__(status.HTTP_422_UNPROCESSABLE_ENTITY, message, detail)

class NotFoundExeption(BaseHTTPException):
    """Not found exception"""
    def __init__(self, message: str = "Resource not found", detail: str = None):
        super().__init__(status.HTTP_404_NOT_FOUND, message, detail)

class ConflictException(BaseHTTPException):
    """Conflict exception (duplicate resources, etc.)"""
    def __init__(self, message: str = "Resource conflict", detail: str = None):
        super().__init__(status.HTTP_409_CONFLICT, message, detail)

class ForbiddenException(BaseHTTPException):
    """Forbidden access exception"""
    def __init__(self, message: str = "Access forbidden", detail: str = None):
        super().__init__(status.HTTP_403_FORBIDDEN, message, detail)

class UnauthorizedException(BaseHTTPException):
    """Unauthorized access exception"""
    def __init__(self, message: str = "Authentication required", detail: str = None):
        super().__init__(status.HTTP_401_UNAUTHORIZED, message, detail)

def setup_exception_handlers(app: FastAPI):
    """Setup global exception handlers"""
    
    @app.exception_handler(BaseHTTPException)
    async def base_http_exception_handler(request: Request, exc: BaseHTTPException):
        """Handle custom HTTP exceptions"""
        logger.error(f"HTTP Exception: {exc.status_code} - {exc.message} - {exc.detail}")
        
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "message": exc.message,
                "detail": exc.detail,
                "status_code": exc.status_code
            }
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handle FastAPI validation errors"""
        errors = []
        for error in exc.errors():
            field = ".".join(str(loc) for loc in error["loc"])
            message = error["msg"]
            errors.append(f"{field}: {message}")
        
        logger.error(f"Validation Error: {errors}")
        
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "success": False,
                "message": "Validation error",
                "detail": errors,
                "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY
            }
        )
    
    @app.exception_handler(ValidationError)
    async def pydantic_validation_exception_handler(request: Request, exc: ValidationError):
        """Handle Pydantic validation errors"""
        errors = []
        for error in exc.errors():
            field = ".".join(str(loc) for loc in error["loc"])
            message = error["msg"]
            errors.append(f"{field}: {message}")
        
        logger.error(f"Pydantic Validation Error: {errors}")
        
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "success": False,
                "message": "Data validation error",
                "detail": errors,
                "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY
            }
        )
    
    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(request: Request, exc: IntegrityError):
        """Handle database integrity errors"""
        logger.error(f"Database Integrity Error: {str(exc)}")
        
        # Parse common integrity errors
        error_msg = str(exc.orig) if exc.orig else str(exc)
        
        if "UNIQUE constraint failed" in error_msg:
            message = "Resource already exists"
            if "email" in error_msg.lower():
                detail = "Email address already registered"
            elif "tracking_code" in error_msg.lower():
                detail = "Tracking code already exists"
            else:
                detail = "Duplicate entry detected"
        else:
            message = "Database constraint violation"
            detail = "The operation violates database constraints"
        
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "success": False,
                "message": message,
                "detail": detail,
                "status_code": status.HTTP_409_CONFLICT
            }
        )
    
    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
        """Handle general SQLAlchemy errors"""
        logger.error(f"Database Error: {str(exc)}")
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": "Database error occurred",
                "detail": "Please try again later",
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
            }
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle unexpected exceptions"""
        logger.error(f"Unexpected Error: {str(exc)}", exc_info=True)
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": "Internal server error",
                "detail": "An unexpected error occurred",
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
            }
        )