import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


def main():
    """
    Main entry point for the application.
    This function starts the FastAPI application.
    """
    uvicorn.run(
        "backend.main:app", host="0.0.0.0", port=8000
    )


def dev():
    """
    Start the development server with hot reload.
    """
    uvicorn.run(
        "backend.main:app", host="127.0.0.1", port=8000, reload=True
    )
