from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import questions, analysis, generation, share
from .database import create_tables
from fastapi.staticfiles import StaticFiles
from .utils.db_loader import init_db
from pathlib import Path


app = FastAPI(title="SinoTale API")

create_tables()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(questions.router, prefix="/api", tags=["questions"])
app.include_router(analysis.router, prefix="/api", tags=["analysis"])
app.include_router(generation.router, prefix="/api", tags=["generation"])
app.include_router(share.router, prefix="/api", tags=["share"])

@app.get("/")
def read_root():
    return {"message": "Welcome to SinoTale API"}


@app.on_event("startup")
async def startup_event():
    init_db()
