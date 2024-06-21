from typing import List
from fastapi import APIRouter, File, UploadFile, HTTPException
from utils.file_utils import process_files
from config import SAVE_DIR


router = APIRouter()

@router.post("/uploads")
async def upload_files(
    tracks: List[UploadFile] = File(None),
    album_covers: List[UploadFile] = File(None), 
    album_booklets: List[UploadFile] = File(None),
    mvs: List[UploadFile] = File(None, allow_multiple=False),
    mv_imgs: List[UploadFile] = File(None, allow_multiple=False)
    ):
    
    if tracks is None:
        raise HTTPException(status_code=400, detail="Tracks not provided")
    if album_covers is None:
        raise HTTPException(status_code=400, detail="Album covers not provided")
    if album_booklets is None:
        raise HTTPException(status_code=400, detail="Album booklets not provided")
    if mvs is None:
        raise HTTPException(status_code=400, detail="MVs not provided")
    if mv_imgs is None:
        raise HTTPException(status_code=400, detail="MV images not provided")
    
    try:
        if not any([tracks, album_covers, album_booklets, mvs, mv_imgs]):
            raise HTTPException(status_code=422, detail="At least one parameter must be provided.")

        response_data = {
            "tracks": await process_files(tracks, "tracks", SAVE_DIR),
            "album_covers": await process_files(album_covers, "album_covers", SAVE_DIR),
            "album_booklets": await process_files(album_booklets, "album_booklets", SAVE_DIR),
            "mvs": await process_files(mvs, "mvs", SAVE_DIR),
            "mv_imgs": await process_files(mv_imgs, "mv_imgs", SAVE_DIR),
        }
        
        # 모든 파일 리스트가 비어 있는지 확인
        all_empty = all(not response_data[key][0] for key in response_data)
        
        # 하나라도 파일이 있으면 success를 True로 설정
        success = not all_empty
        
        if success:
            return {"message": "Files uploaded successfully", **response_data}
        else:
            return {"message": "Failed to upload files", "error": "One or more file uploads failed", **response_data}
    
    
    except HTTPException as e:
        return e