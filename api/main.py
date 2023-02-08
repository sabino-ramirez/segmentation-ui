from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
from ai import config
import base64
import dicom2nifti

from typing import List


class Message(BaseModel):
    content: str
    filenames: list[str]


class Prediction(BaseModel):
    mime: str
    image: str


class PredictionPath(BaseModel):
    # file: str
    pathList: list[str]


# Class Prediction(BaseModel):
#     name: str
#     base64:


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    message = Message(content="Hello Welcome", filenames=[""])
    return message


@app.post("/uploadDicom")
# uploadFile and call ai on it
async def uploadFile(file: UploadFile = File(...)):
    try:
        with open(f"dicoms/{file.filename}", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception:
        return {"error": "exceptioooon"}
    finally:
        file.file.close()

    return {"nice": "hwat is"}

    # config.doTheThing(f"ai/{file.filename}")


@app.get("/showDicom")
async def showDicom():
    dicom2nifti.dicom_series_to_nifti(
        "./dicoms", "./static/dicom.nii.gz", reorient_nifti=True
    )
    # config.dicomHTing()

    filepath = "http://localhost:8000/static/dicom.nii.gz"
    # return PredictionPath(file=filepath)


@app.post("/uploadDicoms")
async def uploadDicoms(files: List[UploadFile] = File(...)):
    print(len(files))
    # for file in files:
    #     try:
    #         with open(f"dicoms/{file.filename}", "wb") as buffer:
    #             shutil.copyfileobj(file.file, buffer)
    #     except Exception:
    #         return {"error": "exceptioooon"}
    #     finally:
    #         file.file.close()
    #
    return {"nice": "hwat is"}


@app.get("/getFile")
# async def returnFile():
#     filePath = "./static/pred_pt19.nii.gz"
#     return FileResponse(filePath)
async def returnFilePath():
    # filePath = "http://localhost:8000/static/pred_pt19.nii.gz"
    vag_path = "http://localhost:8000/static/pt19_label.nii.gz"
    rect_path = "http://localhost:8000/static/pt19_rectum.nii.gz"
    blad_path = "http://localhost:8000/static/pt19_bladder.nii.gz"
    # return PredictionPath(file=filePath)
    return PredictionPath(pathList=[vag_path, rect_path, blad_path])


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
    # return Message(content=f"nice worked")
