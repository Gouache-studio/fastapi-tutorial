# 왜 FastAPI 를 사용하는게 좋은가? 
# 장고와 2배빠르고 코드도 간결하기때문에 사용 

# 비동기처리가 가능. 특정코드가 오래걸리면 일단 제껴두고 다른코드 실행가능 ( 자바스크립트와 비슷하고 성능도비슷)
# 기능도 웹서버만들기 끝 
    # GET POST 요청받기 
    # DB입출력
    # 회원인증
    # 데이터 Validation
    # 웹소켓
    # async/await
    
    # type넣기
    # API 문서 자동생성 
    
# 웹프레임워크보다는 웹개발'툴'로 인식
# 장고처럼 크게 개발하는것보다는 작은 기능으로 나눠서 하는게 유행..

from fastapi import FastAPI
app = FastAPI()

from fastapi.responses import FileResponse

# 기능추가 메인페이지 접속시 'hello' 보내기
@app.get("/")
def 작명():
    return 'hello'

@app.get("/data")
def 작명():
    return {'hello' : 1224}

# html 페이지 접속시 html 파일 전송?
@app.get("/html")
def 작명():
    return FileResponse('index.html') # 파일경로

# 유저한테 데이터를 받고싶을때? 이름하고 이름을 받으려면? post로 써서 서버로 보내는것임. 
# 하지만 그냥 받을수가 없음. 모델부터 생성필요
# 어떤 모델이 필요 밑에 있는 거 참조 할것
# 타입을 정함으로서 타입에러 잡아낼수있음
from pydantic import BaseModel

class Model(BaseModel):
    name  : str
    phone : int

@app.post("/send")
def 작명(data : Model):
    print(data)
    return '전송완료'

# 또한 DB접속도 가능! 
# DB접속해주세요~~~

@app.get("/aaa")
async def 작명():
    # DB에서 데이터 꺼내주세요~~~ 
    # await 를 이용해서 비동기 처리도 가능함 즉, async - await 조합으로 비동기처리가 가능함
    return FileResponse('index.html')

