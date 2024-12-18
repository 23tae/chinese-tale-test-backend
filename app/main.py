from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import questions, analysis
from .database import create_tables
from fastapi.staticfiles import StaticFiles
from .utils.db_loader import init_db


app = FastAPI(title="Chinese Tale Test API")

create_tables()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(questions.router, prefix="/api", tags=["질문지"])
app.include_router(analysis.router, prefix="/api", tags=["캐릭터 선정"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Chinese Tale Test API"}


@app.on_event("startup")
async def startup_event():
    init_db()
