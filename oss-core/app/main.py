import logging
from fastapi import FastAPI
from app.controllers import bss_controller

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s] 🧠 %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Create the main FastAPI application instance
app = FastAPI(
    title="OSS Playground API",
    description="A toy project mimicking OSS middleware behavior.",
    version="1.0.0"
)

# Include the router from bss_controller (Hiring the clerk)
app.include_router(bss_controller.router)

@app.get("/")
async def root():
    return {"message": "OSS Playground is running."}