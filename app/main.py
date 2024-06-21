from fastapi import FastAPI, Request, HTTPException
from routers import uploads
import httpx, logging, certifi

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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


# Saleforce -> YGP
@app.post("/buptle-management/contract", tags=["buptle-management"])
async def get_buptle_contract(request: Request):
    try:
        data = await request.json()
        print(data)
        return {"message": "Salesforce 데이터 잘받음", "data": data}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# YGP -> YG
@app.post("/buptle-management/sf", tags=["buptle-management"])
async def get_contract_data():
    
    EXTERNAL_API_URL = "http://183.96.217.93/api/external-company/save"
    encoded_token    = "WUdQOmVXZHdPbmxuY0RJd01qUXdOakV5SVE9PQ=="
    
    params           = {
                            "request_seq"               : "1",
                            "external_system_key_value" : "103",
                            "name"                      : "(주)XX전자",
                            "ceo_name"                  : "홍길동",
                            "create_time"               : "20231231120000"
                       }
    
    async with httpx.AsyncClient(follow_redirects=True, verify=False) as client:
        try:
            
            headers = {
                "Authorization": f"Base {encoded_token}"
            }
            logger.info(f"\nSending POST to {EXTERNAL_API_URL} with params: {params}\n")
            response = await client.post(EXTERNAL_API_URL, headers=headers, params=params)
            logger.info(f"\n response ::: {response} \n")
            response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
            logger.info("Request POST successful")
            data = response.json()
            
            return {"message": "Data fetched successfully", "data": data}
        
        except httpx.HTTPStatusError as http_err:
            
            logger.error(f"HTTPStatusError: {http_err}")
            logger.error(f"Response content: {response.text}")
            raise HTTPException(status_code=response.status_code, detail=str(http_err))
            
        except Exception as e:
            logger.error(f"Exception: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)