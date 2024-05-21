from fastapi import FastAPI

from src.endpoints import health, auth, example
from src.config import Settings

app = FastAPI()

"""
The configure_app function is responsible for configuring the FastAPI app with the CORS middleware and database 
settings.
"""
Settings().configure_app(app)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(example.router)
