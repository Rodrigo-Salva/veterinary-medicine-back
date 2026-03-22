from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.infrastructure.adapters.api.routes import router

app = FastAPI(title="Veterinary System API", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Veterinary System API"}
