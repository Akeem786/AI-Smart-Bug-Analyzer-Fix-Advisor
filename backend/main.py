from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from routes.upload import router as upload_router
from routes.analyze import router as analyze_router
from routes.health import router as health_router

app = FastAPI(
    title="AI Defect Analysis System",
    description="Intelligent Bug Triage, Log Diagnostics, Root Cause & Remediation Advisor",
    version="1.0.0"
)

# Configure CORS Middleware for React frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Internal Server Error",
            "detail": str(exc)
        }
    )

# Register Routes
app.include_router(upload_router)
app.include_router(analyze_router)
app.include_router(health_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to AI Defect Analysis System",
        "status": "Running",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "submit": "/submit",
            "analyze": "/analyze",
            "submit_and_analyze": "/submit-and-analyze",
            "docs": "/docs"
        }
    }