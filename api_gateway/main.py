from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import httpx

app = FastAPI()

# @app.get("/proxy")
# async def proxy(request: Request):
#     # Extract the JWT token from the request headers
#     auth_header = request.headers.get("Authorization")
#     if not auth_header:
#         raise HTTPException(status_code=401, detail="Missing Authorization header")

#     token = auth_header.split(" ")[1]
    
#     # Decode the JWT token to get the user ID
#     try:
#         payload = jwt.decode(token, options={"verify_signature": False})
#         user_id = payload.get("sub")
#         if not user_id:
#             raise HTTPException(status_code=401, detail="Invalid token")
#     except jwt.ExpiredSignatureError:
#         raise HTTPException(status_code=401, detail="Token has expired")
#     except jwt.InvalidTokenError:
#         raise HTTPException(status_code=401, detail="Invalid token")

#     # Forward the request to another service
#     async with httpx.AsyncClient() as client:
#         response = await client.get("https://example.com/api", headers=request.headers)
    
#     return response.json()

@app.get("/proxy")
async def proxy(request: Request):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")
    
    # Forward to downstream service
    async with httpx.AsyncClient() as client:
        resp = await client.get("http://service-a:8001/data", headers={"Authorization": token})
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail="Error from downstream service")
    return JSONResponse(status_code=resp.status_code, content=resp.json())

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )