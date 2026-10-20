import logging

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


class NotFoundError(Exception):
    """El recurso solicitado en la URL no existe (ej. GET /tasks/99999)."""


class InvalidReferenceError(Exception):
    """El body referencia un recurso que no existe (ej. category_id inexistente)."""


def register_exception_handlers(app: FastAPI) -> None:
    """Traduce las excepciones de dominio a respuestas HTTP con formato {"detail": ...}.

    Así los services no conocen HTTP: solo lanzan la excepción y aquí se decide el código.
    """

    @app.exception_handler(NotFoundError)
    async def handle_not_found(_: Request, exc: NotFoundError) -> JSONResponse:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)})

    @app.exception_handler(InvalidReferenceError)
    async def handle_invalid_reference(_: Request, exc: InvalidReferenceError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, content={"detail": str(exc)}
        )

    @app.exception_handler(Exception)
    async def handle_unexpected(_: Request, exc: Exception) -> JSONResponse:
        # Red de seguridad: si algo falla sin control, se registra el error real en consola
        # y el cliente recibe un mensaje limpio en vez de un stack trace.
        logger.exception("Error no controlado: %s", exc)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Error interno del servidor"},
        )
