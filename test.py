import uvicorn
import jwt

from datetime import datetime, timedelta, timezone
from typing import Union, Any
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

from security import validate_token

SECURITY_ALGORITHM = 'HS256'
SECRET_KEY = '123456'

app = FastAPI(
    title='FastAPI JWT Example', openapi_url='/api/v1/openapi.json', docs_url='/api/v1/docs',
    description='FastAPI JWT Example'
)

class LoginRequest(BaseModel):
    username: str
    password: str

def generate_jwt_token(username: Union[str, Any]) -> str:
    expire = datetime.now(tz=timezone.utc) + timedelta(
        seconds=60 * 60 * 24 * 3 # Expire in 3 days
    )
    to_encode = {
        'exp': expire,
        'username': username
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=SECURITY_ALGORITHM)
    return encoded_jwt
   
def verify_password(username: str, password: str) -> bool:
    # Simulate a password verification process
    return username == 'admin' and password == 'admin'

@app.post('/login')
def login(request: LoginRequest):
    # Simulate a login process
    if verify_password(request.username, request.password):
        token = generate_jwt_token(request.username)
        return {
            'token': token
        }
    raise HTTPException(status_code=404, detail='User not found')

@app.get('/books', dependencies=[Depends(validate_token)])
def list_books():
    return {'books': ['Book 1', 'Book 2', 'Book 3']}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)