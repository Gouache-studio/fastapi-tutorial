import os
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from typing import List, Optional

app = FastAPI()

# 파일을 저장할 경로 지정
SAVE_DIR = "/Users/mac/Desktop/Gromit/_02_STUDY/_05_SideProject/FastAPI/NAS/"

@app.post("/upload")
async def upload_files(
    tracks : Optional[List[UploadFile]] = File(...), 
    album_covers : Optional[List[UploadFile]] = File(...), 
    album_booklets  : Optional[List[UploadFile]] = File(...)):
    
    response_data = {"tracks": [], "album_cover": [], "album_booklets": []}
    success = True
    
    # 음원 파일 처리 로직
    if tracks is not None:
        for track in tracks:
            save_path = os.path.join(SAVE_DIR, track.filename)
            with open(save_path, "wb") as f:
                contents = await track.read()
                f.write(contents)
            response_data["tracks"].append({"filename": track.filename, "save_path": save_path})
    
    # 이미지 파일 처리 로직
    if album_covers is not None:
        for album_cover in album_covers :
            pass
    
    # 텍스트 파일 처리 로직
    if album_booklets is not None:
        for album_booklet in album_booklets:
            pass
    
    if success:
        return {"message": "Files uploaded successfully", **response_data}
    else:
        return {"message": "Failed to upload files", "error": "Reason for failure"}


