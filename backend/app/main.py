
from fastapi import FastAPI
from app.routes import products
from app.routes import auth
from app.database import Base, engine
from app import models

Base.metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI(
    title="NexCart API",
    description="Backend API for the E-Commerce Website",
    version="1.0.0"
)

#Register product routes
app.include_router(products.router)
app.include_router(auth.router)

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
