
from fastapi import FastAPI

# Initialize FastAPI application
app = FastAPI(
    title="NexCart API",
    description="Backend API for the E-Commerce Website",
    version="1.0.0"
)

# Root endpoint
@app.get("/")
def home():
    return {
        "message": "Welcome to NexCart E-Commerce API",
        "status": "Running successfully"
    }

# Health check endpoint
@app.get("/health")
def health_check():
    return {
        "status": "Healthy"
    }
