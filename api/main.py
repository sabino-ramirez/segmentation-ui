from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil

# from typing import List


class Message(BaseModel):
    content: str


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
    # message = Message(content="Hello Welcome")
    return FileResponse("/home/sabino/papaya-react/build/index.html")
    # return message


@app.post("/upload", response_model=Message)
def uploadFile(file: UploadFile = File(...)):
    try:
        with open(f"ai/{file.filename}", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    # message = Message(content=f"Successfully uploaded {file.filename}")
    # return message
    return Message(content=f"Successfully uploaded {file.filename}")
    # return {"message": f"Successfully uploaded {file.filename}"}


@app.get("/infer")
async def getInference():
    slices = [
        FileResponse(f"ai/predictions/pred_slice_{i}.png", filename=f"slice{i}.png")
        for i in range(1, 13)
    ]
    return slices


# upload list of files
# from yt video of russian guy
