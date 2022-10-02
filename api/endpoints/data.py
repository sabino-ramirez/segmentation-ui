from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from pydantic import BaseModel

router = APIRouter(
    prefix="/data",
    tags=['Data']
)

class Image(BaseModel):
    name: str
    type: str

class Message(BaseModel):
    name: str
    size: str

router.post("/upload")
async def getPrediction(image: Image):
    return image
