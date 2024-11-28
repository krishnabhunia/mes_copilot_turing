from fastapi import FastAPI, File, UploadFile
import shutil
from pathlib import Path

app = FastAPI()
UPLOAD_PATH = Path("uploaded_files")

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    UPLOAD_PATH.mkdir(parents=True, exist_ok=True)
    file_path = UPLOAD_PATH / file.filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename}
