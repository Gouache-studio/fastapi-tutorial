import os
from fastapi import UploadFile

async def save_file(file: UploadFile, save_dir: str):
    save_path = os.path.join(save_dir, file.filename)
    with open(save_path, "wb") as f:
        contents = await file.read()
        f.write(contents)
    return save_path