from fastapi import FastAPI, Request, HTTPException
from app.routers import uploads


app = FastAPI() 

# app.include_router(items.router, prefix='/items', tags=["items"])
app.include_router(uploads.router, prefix='/album-management', tags=["album-management"]) # tag는 docs에서 사용


# 기본 루트
@app.get("/")
def read_root():
    return {"Hello": "World"}


# DSP 전송 API
# 1. Saleforce에서 json데이터를 가져온다.
# 2. 모델을 통해 데이터 검증로직을 추가한다.
# 3. 전송큐에 있는 폼에 맞춰서 json 변경 
# 4. 전송큐에 데이터 전송


@app.post("/album-management/dsp", tags=["album-management"])
async def get_dsp_data(request: Request):
    try:
        data = await request.json()
        print(data)
        return {"message": "DSP data received", "data": data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)