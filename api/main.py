from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
from ai import config
import base64

# from typing import List


class Message(BaseModel):
    content: str


class Prediction(BaseModel):
    mime: str
    image: str


class PredictionPath(BaseModel):
    file: str


# Class Prediction(BaseModel):
#     name: str
#     base64:


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
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
    message = Message(content="Hello Welcome")
    return message


@app.post("/upload", response_model=Message)
# async def uploadFile(img: str):
#     config.doTheThing(img)
#
#     with open("ai/pred_"+img, "rb") as image_file:
#         encoded_image_string = base64.b64encode(image_file.read())
#
#     payload = {"image": encoded_image_string}
#     # return Message(content=f"Successfully uploaded {file.filename}")
#     return payload


def uploadFile(file: UploadFile = File(...)):
    try:
        with open(f"ai/{file.filename}", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    config.doTheThing(f"ai/{file.filename}")


@app.get("/getFile")
# async def returnFile():
#     filePath = "./static/pred_pt19.nii.gz"
#     return FileResponse(filePath)
async def returnFilePath():
    # filePath = "http://localhost:8000/static/pred_pt19.nii.gz"
    filePath = "http://localhost:8000/static/pt19_label.nii.gz"
    return PredictionPath(file=filePath)


@app.get("/test")
async def returnBase64():
    # content = myFile.file.read()
    with open("pred_pt19.nii.gz", "rb") as f:
        converted = base64.b64encode(f.read())

    # print(type(converted))
    # print(converted)
    print(str(converted, encoding="latin-1"))
    # f.write(content)

    return Prediction(mime="image/nii", image=f"{str(converted, encoding='utf-8')}")


@app.get("/infer")
async def getInference():
    # config.print_config()
    config.doTheThing("pt19.nii.gz")
    return Message(content=f"nice worked")
