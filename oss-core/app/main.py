from fastapi import FastAPI
from app.receivers import http_receiver

# Create the main FastAPI application instance
app = FastAPI(
    title="OSS Playground API",
    description="A toy project mimicking ShinOSS/Nokia OSS middleware behavior.",
    version="1.0.0"
)

# Include the router from http_receiver (Hiring the clerk!)
app.include_router(http_receiver.router)

@app.get("/")
async def root():
    return {"message": "OSS Playground is running."}