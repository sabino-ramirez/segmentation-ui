from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from endpoints import data

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Image(BaseModel):
    name: str
    type: str

class Message(BaseModel):
    name: str
    size: str

@app.get("/")
async def root():
    return {"message": "Hello boyis"}

@app.post("/upload")
async def getPrediction(image: Image):
    return image
