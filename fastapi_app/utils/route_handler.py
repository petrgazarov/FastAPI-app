from typing import Callable, Coroutine, Any
from fastapi import Request, Response, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.routing import APIRoute
from .logger import AppLogger

logger = AppLogger().get_logger()


# log request body on validation error
class ValidationErrorLoggingRoute(APIRoute):
    def get_route_handler(self) -> Callable[[Request], Coroutine[Any, Any, Response]]:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                return await original_route_handler(request)
            except RequestValidationError as exc:
                body = await request.body()
                detail = {"errors": exc.errors(), "body": body.decode()}
                logger.error(detail)
                raise HTTPException(status_code=422, detail=detail)

        return custom_route_handler
