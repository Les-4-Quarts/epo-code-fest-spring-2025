import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from api.resources import patent_resource


tags_metadata = [
    {
        "name": "Patents",
        "description": "Operations with patents.",
    },
    {
        "name": "Health",
        "description": "Health check endpoint.",
    },
]

app = FastAPI(
    title="Compass for European Patents",
    description="API for managing and retrieving European patents.",
    version="1.0.0",
    openapi_tags=tags_metadata,
    docs_url="/api/docs",
)

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

router = APIRouter(
    prefix="/api",
)
router.include_router(patent_resource.router)


@router.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint to verify if the API is running.
    """
    return {"status": "ok"}


app.include_router(router)


def main():
    """
    Main entry point for the application.
    This function starts the FastAPI application.
    """
    uvicorn.run(
        "api.main:app", host="0.0.0.0", port=8000
    )


def dev():
    """
    Start the development server with hot reload.
    """
    uvicorn.run(
        "api.main:app", host="127.0.0.1", port=8000, reload=True
    )
