from pydantic import BaseModel
from fastapi.responses import JSONResponse


def GenericError(details: str, code: int = 500) -> JSONResponse:
    return JSONResponse({"status": "error", "details": details}, code)
