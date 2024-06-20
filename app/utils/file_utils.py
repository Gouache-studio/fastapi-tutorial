from fastapi import UploadFile
from typing import List
import os

async def save_file(file: UploadFile, save_dir: str) -> str:
    save_path = os.path.join(save_dir, file.filename)
    with open(save_path, "wb") as f:
        contents = await file.read()
        f.write(contents)
    return save_path

async def process_files(file_list: List[UploadFile], file_type: str, save_dir: str) -> List[dict]:
    if file_list is None or len(file_list) == 0 or file_list[0].filename == "":
        return[{
            "error": {
                        "status": 400,
                        "detail": "InvalidParameter",
                        "message": "No album_booklets files found for the given parameter."
                     }
            }]   
        
    response = []
    for idx, file in enumerate(file_list, start=1):
        try:
            save_path = await save_file(file, save_dir)
            response.append({
                "status": 200,
                "data": {
                            "id": idx,
                            "fileName": file.filename,
                            "savePath": save_path,
                            "url": "https://unify-api.ygplus.com" + save_path
                        }
            })
        except Exception as e:
            response.append({
                "error" : {
                    "status" : 500, 
                    "error": str(e), 
                    "message": f"Failed to upload {file_type}files. Check Server Code"
                    }
                })
    return response
