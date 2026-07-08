from fastapi import FastAPI

from routes.upload import router as upload_router
from routes.analyze import router as analyze_router
from routes.health import router as health_router

app = FastAPI(
    title="AI Defect Analysis System",
    description="Milestone 1 - Bug Submission & RAG Prototype",
    version="1.0.0"
)

# Register Routes
app.include_router(upload_router)
app.include_router(analyze_router)
app.include_router(health_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to AI Defect Analysis System",
        "status": "Running"
    }