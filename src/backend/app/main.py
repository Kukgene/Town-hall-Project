"""Main entry point of api server"""
from fastapi import FastAPI

from .routers import recycle


app = FastAPI(title="Town Hall Project")

app.include_router(recycle.router)
