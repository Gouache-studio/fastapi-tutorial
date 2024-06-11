import os, re
from pydantic import BaseModel
from typing import Union
from fastapi import FastAPI, File, UploadFile, HTTPException
from typing import List, Optional


class Item(BaseModel):
    name: str
    description: str
    
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/start/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

# 파일을 저장할 경로 지정
SAVE_DIR = "/Users/mac/Desktop/Gromit/_02_STUDY/_05_SideProject/FastAPI/NAS/"    

async def save_files(files: Optional[List[UploadFile]], category: str, response_data: dict):
    if files is None:
        response_data[category].append({"code": "parameter", "message": f"Failed to receive {category.upper()} uploaded"})
        return False

    if not files or not files[0].filename:
        response_data[category].append({"message": f"No {category} files found for parameter"})
        return True

    for idx, file in enumerate(files, start=1):
        try:
            save_path = os.path.join(SAVE_DIR, file.filename)
            with open(save_path, "wb") as f:
                contents = await file.read()
                f.write(contents)
            response_data[category].append({
                "no": idx,
                "file_name": file.filename,
                "save_path": save_path,
                "url": f"https://unify-api.ygplus.com{save_path}"
            })
        except Exception as e:
            response_data[category].append({"message": "Failed to upload files", "error": str(e)})
            return False
    return True

@app.post("/upload")
async def upload_files(
    tracks: List[UploadFile] = File(None),
    album_covers: List[UploadFile] = File(None), 
    album_booklets: List[UploadFile] = File(None),
    mvs: List[UploadFile] = File(None, allow_multiple=False),
    mv_imgs: List[UploadFile] = File(None, allow_multiple=False)
):
    response_data = {
        "tracks": [], 
        "album_covers": [], 
        "album_booklets": [], 
        "mvs": [], 
        "mv_imgs": []
    }
    
    success = True
    
    success &= await save_files(tracks, "tracks", response_data)
    success &= await save_files(album_covers, "album_covers", response_data)
    success &= await save_files(album_booklets, "album_booklets", response_data)
    success &= await save_files(mvs, "mvs", response_data)
    success &= await save_files(mv_imgs, "mv_imgs", response_data)

    if success:
        return {"message": "Files uploaded successfully", **response_data}
    else:
        return {"message": "Failed to upload files", "error": "Unknown error"}
       
# @app.post("/upload")
# async def upload_files(
#     tracks         : List[UploadFile] = File(None),
#     album_covers   : List[UploadFile] = File(None), 
#     album_booklets : List[UploadFile] = File(None),
#     mvs            : List[UploadFile] = File(None, allow_multiple=False),
#     mv_imgs        : List[UploadFile] = File(None, allow_multiple=False)
#     ):
    
#     response_data = {
#                         "tracks": [], 
#                         "album_covers": [], 
#                         "album_booklets": [], 
#                         "mvs" : [], 
#                         "mv_imgs" : []
#                     }
#     success = True
    
#     if tracks is None:
#         response_data["tracks"].append({"code" : "parameter", "message" : "Failed to receive TRACKS uploaded"})
#     if album_covers is None:
#         response_data["album_covers"].append({"code" : "parameter", "message" : "Failed to receive ALBUM_COVERS uploaded"})
#     if album_booklets is None:
#         response_data["album_booklets"].append({"code" : "parameter", "message" : "Failed to receive ALBUM_BOOKLETS uploaded"})
#     if mvs is None:
#         response_data["mvs"].append({"code" : "parameter", "message" : "Failed to receive MV uploaded"})
#     if mv_imgs is None:
#         response_data["mv_imgs"].append({"code" : "parameter", "message" : "Failed to receive MV_IMGS uploaded"})

#     # tracks 처리로직
#     if tracks is not None:
#         if str(tracks[0].filename) != "":
#             for idx, track in enumerate(tracks, start=1):
#                 try:
#                     save_path = os.path.join(SAVE_DIR, track.filename)
#                     with open(save_path, "wb") as f:
#                         contents = await track.read()
#                         f.write(contents)
#                     response_data["tracks"].append({"no" : idx,  "file_name": track.filename, "save_path": save_path, "url" : "https://unify-api.ygplus.com"+save_path})
#                 except Exception as e:
#                     success = False
#                     response_data["tracks"].append({"message": "Failed to upload files", "error": str(e)})
#         else:
#             response_data["tracks"].append({"message" : "No track files found for parameter"})

#     # album_covers 처리로직
#     if album_covers is not None:
#         if str(album_covers[0].filename) != "":
#             for idx, track in enumerate(album_covers, start=1):
#                 try:
#                     save_path = os.path.join(SAVE_DIR, track.filename)
#                     with open(save_path, "wb") as f:
#                         contents = await track.read()
#                         f.write(contents)
#                     response_data["album_covers"].append({"no" : idx,  "file_name": track.filename, "save_path": save_path, "url" : "https://unify-api.ygplus.com"+save_path})
#                 except Exception as e:
#                     success = False
#                     response_data["album_covers"].append({"message": "Failed to upload files", "error": str(e)})
#         else:
#             response_data["album_covers"].append({"message" : "No album_covers files found for parameter"})
    
#     # album_booklets 처리로직
#     if album_booklets is not None:
#         if str(album_booklets[0].filename) != "":
#             for idx, track in enumerate(album_booklets, start=1):
#                 try:
#                     save_path = os.path.join(SAVE_DIR, track.filename)
#                     with open(save_path, "wb") as f:
#                         contents = await track.read()
#                         f.write(contents)
#                     response_data["album_booklets"].append({"no" : idx,  "file_name": track.filename, "save_path": save_path, "url" : "https://unify-api.ygplus.com"+save_path})
#                 except Exception as e:
#                     success = False
#                     response_data["album_booklets"].append({"message": "Failed to upload files", "error": str(e)})
#         else:
#             response_data["album_booklets"].append({"message" : "No album_booklets files found for parameter"})
    
#     # mv 처리로직
#     if mvs is not None:
#         if str(mvs[0].filename) != "":
#             for idx, track in enumerate(mvs, start=1):
#                 try:
#                     save_path = os.path.join(SAVE_DIR, track.filename)
#                     with open(save_path, "wb") as f:
#                         contents = await track.read()
#                         f.write(contents)
#                     response_data["mvs"].append({"no" : idx,  "file_name": track.filename, "save_path": save_path, "url" : "https://unify-api.ygplus.com"+ save_path})
#                 except Exception as e:
#                     success = False
#                     response_data["mvs"].append({"message": "Failed to upload files", "error": str(e)})
#         else:
#             response_data["mvs"].append({"message" : "No mvs files found for parameter"})
    
#     # mv_imgs 처리로직
#     if mv_imgs is not None:
#         if str(mv_imgs[0].filename) != "":
#             for idx, track in enumerate(mv_imgs, start=1):
#                 try:
#                     save_path = os.path.join(SAVE_DIR, track.filename)
#                     with open(save_path, "wb") as f:
#                         contents = await track.read()
#                         f.write(contents)
#                     response_data["mv_imgs"].append({"no" : idx,  "file_name": track.filename, "save_path": save_path, "url" : "https://unify-api.ygplus.com"+save_path})
#                 except Exception as e:
#                     success = False
#                     response_data["mv_imgs"].append({"message": "Failed to upload files", "error": str(e)})
#         else:
#             response_data["mv_imgs"].append({"message" : "No mv_imgs files found for parameter"})
    
#     if success:
#         return {"message": "Files uploaded successfully", **response_data}
#     else:
#         return {"message": "Failed to upload files", "error": "Unkown error"}


