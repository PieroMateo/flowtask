import logging

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


# lo que se pide en la url no existe, ej: GET /tasks/99999
class NotFoundError(Exception):
    pass


# el body apunta a algo que no existe, ej: un category_id que no esta en la bd
class InvalidReferenceError(Exception):
    pass


# los services solo lanzan estas excepciones y aqui se decide que codigo http responder,
# por eso los services no importan nada de fastapi
def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(NotFoundError)
    async def handle_not_found(_: Request, exc: NotFoundError) -> JSONResponse:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)})

    @app.exception_handler(InvalidReferenceError)
    async def handle_invalid_reference(_: Request, exc: InvalidReferenceError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, content={"detail": str(exc)}
        )

    # por si algo falla y no lo teniamos previsto: el error real queda en la consola
    # y al cliente le llega un mensaje simple, sin detalles internos
    @app.exception_handler(Exception)
    async def handle_unexpected(_: Request, exc: Exception) -> JSONResponse:
        logger.exception("Error no controlado: %s", exc)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Error interno del servidor"},
        )
