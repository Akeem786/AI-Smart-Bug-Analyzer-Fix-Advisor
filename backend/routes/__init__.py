from fastapi import FastAPI
from routes.upload import router as upload_router

app = FastAPI(
    title="AI Defect Analysis System",
    description="Milestone 1 - Bug Submission & RAG Prototype",
    version="1.0.0"
)

app.include_router(upload_router)

@app.get("/")
def home():
    return {
        "message": "Welcome to AI Defect Analysis System",
        "status": "Running"
    }

@app.get("/health")
def health():
    return {
        "status": "OK"
    }