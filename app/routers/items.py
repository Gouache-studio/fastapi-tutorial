from fastapi import APIRouter
from fastapi.responses import FileResponse
from typing import Union
from models.items import Item


router = APIRouter()

@router.get("/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@router.get("/get", response_model=Item)
def read_item():
    return FileResponse('/Users/mac/Desktop/GROMIT/_00_SideProject/01_FastAPI/index.html')

@router.post("/send")
def send_item(data:Item):
    print(data)
    return "전송완료"