from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import shutil
import uvicorn

class Message(BaseModel):
    name: str
    size: str

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


@app.get("/")
async def root():
    return {"message": "Hello boyis"}

@app.post("/upload")
async def getPrediction(file: UploadFile = File(...)):
    with open(f'{file.filename}', 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"message": "file saved"}

@app.get("/infer")
async def getInference():

    return {"message": "inference successful"}

# upload list of files
# from yt video of russian guy
