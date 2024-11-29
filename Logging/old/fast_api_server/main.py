# from fastapi import FastAPI, UploadFile, File
# import shutil
# from pathlib import Path

# app = FastAPI()

# UPLOAD_PATH = "/app/uploads"

# @app.post("/upload/")
# async def upload_file(file: UploadFile = File(...)):
#     Path(UPLOAD_PATH).mkdir(parents=True, exist_ok=True)
#     file_path = f"{UPLOAD_PATH}/{file.filename}"
#     with open(file_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)
#     return {"filename": file.filename, "path": file_path}
