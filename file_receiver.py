import os
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse

app = FastAPI()

# 파일을 저장할 경로 지정
# SAVE_DIR = "/Users/mac/Desktop/Gromit/_02_STUDY/_05_SideProject/FastAPI/NAS/"
script_dir = os.path.dirname(os.path.abspath(__file__))
# NAS 폴더의 상위 폴더로 이동한 상대 경로
relative_dir = os.path.join("..", "NAS")
# 상대 경로를 절대 경로로 변환하여 저장 경로 설정
SAVE_DIR = os.path.abspath(os.path.join(script_dir, relative_dir))

@app.post("/upload")

async def upload_file(file: UploadFile = File(...)):
    print(file.filename)
    # 파일을 읽어서 저장할 경로 지정
    save_path = os.path.join(SAVE_DIR, file.filename)
    
    # 파일을 저장
    with open(save_path, "wb") as f:
        contents = await file.read()
        f.write(contents)
    
    return {"filename": file.filename, "save_path": save_path}



