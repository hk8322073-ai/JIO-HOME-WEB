import aiohttp

from fastapi import FastAPI, Request
from contextlib import asynccontextmanager

from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic_core import ValidationError

from routes.api import apiRoute
from api.client import client

@asynccontextmanager                            # For maintaining one TCP Session For all http req
async def lifespan(app: FastAPI):
    client.session = aiohttp.ClientSession()
    yield
    await client.session.close()

app = FastAPI(
    title="JIO-HOME-WEB API",
    description="Jio Home Authentication and Device Management API",
    version="1.0.0",
    lifespan=lifespan
)

# Calls automatically once when app starts & stops
app.mount("/public", StaticFiles(directory="public"), name="public")
app.include_router(apiRoute, prefix="/api")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "service": "JIO-HOME-WEB API"
    }

@app.exception_handler(StarletteHTTPException)   # Manage all invalid API endpoint requests
async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException
):
    if request.method == "GET":
        return FileResponse(
            "templates/404.html",
            status_code = 404
        )
        
    if exc.status_code == 404:
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "message": "Invalid API endpoint.",
                "status_code": 404
            },
        )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
            "status_code": exc.status_code
        },
    )

@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    """Handle validation errors."""
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Validation error",
            "status_code": 422,
            "details": exc.errors()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error",
            "status_code": 500
        }
    )