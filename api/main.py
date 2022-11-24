from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
from ai import config
import base64

# from typing import List


class Message(BaseModel):
    content: str


# Class Prediction(BaseModel):
#     name: str
#     base64:


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


@app.get("/test")
async def returnBase64(imgName: str = "none"):
    if imgName == "none":
        print("didn't work")
    else:
        # content = myFile.file.read()
        with open('pt19.nii.gz', 'rb') as f: 
            converted = base64.b64decode(f.read())

        print(type(converted))
        print(converted)
            # f.write(content)
    
    return Message(content=f"nice worked")

@app.get("/infer")
async def getInference():
    # config.print_config()
    config.doTheThing("pt19.nii.gz")
    return Message(content=f"nice worked")


# @app.get("/infer")
# async def getInference():
#     slices = [
#         FileResponse(f"ai/predictions/pred_slice_{i}.png", filename=f"slice{i}.png")
#         for i in range(1, 13)
#     ]
#     return slices


# upload list of files
# from yt video of russian guy
