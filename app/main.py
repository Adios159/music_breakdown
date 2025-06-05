import os
import shutil
import subprocess
import uuid
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/separate")
async def separate(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    input_path = os.path.join(OUTPUT_DIR, f"{file_id}_{file.filename}")
    with open(input_path, "wb") as f:
        content = await file.read()
        f.write(content)

    stem_out = os.path.join(OUTPUT_DIR, file_id)
    os.makedirs(stem_out, exist_ok=True)

    # Use demucs 6-stem model for separation
    command = [
        "python3", "-m", "demucs.separate",
        "--model", "htdemucs_6s",
        "--out", stem_out,
        input_path
    ]
    try:
        subprocess.run(command, check=True)
    except Exception as e:
        return {"error": str(e)}

    # Compress results for download
    archive_path = shutil.make_archive(stem_out, 'zip', stem_out)
    return FileResponse(archive_path, filename=f"{file.filename}_stems.zip")
