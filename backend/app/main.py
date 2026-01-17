from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()

# Mount static folder
app.mount("/", StaticFiles(directory="static", html=True), name="static")

# Upload folder
UPLOAD_FOLDER = Path("uploads")
UPLOAD_FOLDER.mkdir(exist_ok=True)

@app.get("/api/ping")
def ping():
    return {"message": "backend is alive"}

@app.post("/api/save-video")
async def save_video(file: UploadFile = File(...)):
    file_location = UPLOAD_FOLDER / file.filename
    with open(file_location, "wb") as f:
        f.write(await file.read())
    return {"status": "saved", "filename": file.filename}
