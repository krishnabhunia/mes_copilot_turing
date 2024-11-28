from fastapi import FastAPI, File, UploadFile
import os

app = FastAPI()

UPLOAD_PATH = "/data"  # Path to save files inside docker volume

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    os.makedirs(UPLOAD_PATH, exist_ok=True)
    file_path = os.path.join(UPLOAD_PATH, file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    return {"filename": file.filename, "path": file_path}
