from fastapi import FastAPI, Request, HTTPException
import jwt
import httpx

app = FastAPI()

GOOGLE_JWkS_URL = "https://www.googleapis.com/oauth2/v3/certs"

@app.get("/data")
async def protected_data(request: Request):
    auth = request.heders.get("Authorization")
    if not auth:
        raise HTTPException(status_code=403, detail="Missing token")

    token = auth.split(" ")[1]
    # try:
    #     # Fetch Google's public keys
    #     async with httpx.AsyncClient() as client:
    #         response = await client.get(GOOGLE_JWkS_URL)
    #         response.raise_for_status()
    #         jwks = response.json()

    #     # Decode the JWT token using the public keys
    #     decoded_token = jwt.decode(token, jwks, algorithms=["RS256"], audience="your-client-id")
    #     return {"message": "Protected data", "user": decoded_token}
    # except jwt.ExpiredSignatureError:
    #     raise HTTPException(status_code=401, detail="Token expired")
    # except jwt.InvalidTokenError:
    #     raise HTTPException(status_code=401, detail="Invalid token")
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))
    async with httpx.AsyncClient() as client:
        jwks = (await client.get(GOOGLE_JWkS_URL)).json()
        try:
            decoded = jwt.decode(token, jwks["keys"][0], algorithms=["RS256"], audience="your-client-id")
        except Exception as e:
            raise HTTPException(status_code=401, detail="Invalid token")
    return {"message": "Hello from Service A!", "user": decoded.get("email")}