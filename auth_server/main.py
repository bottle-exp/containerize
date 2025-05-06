import os
import redis
import json
import secrets
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Env variables
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIS_HOST = os.getenv("REDIS_HOST", "local")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")

# Redis client
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

app = FastAPI(
    title='FastAPI JWT Example', openapi_url='/api/v1/openapi.json', docs_url='/api/v1/docs',
    description='FastAPI JWT Example'
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:9000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add SessionMiddleware
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET_KEY", "your-secret-key"),  # Replace with a secure key
)

config = Config(".env")

oauth = OAuth(config)
oauth.register(
    name="google",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
    authorize_params={"access_type": "offline"},  # Request offline access to get a refresh_token
)

@app.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth")
    nonce = secrets.token_hex(16)  # Generate a nonce
    request.session["nonce"] = nonce  # Store the nonce in the session
    return await oauth.google.authorize_redirect(request, redirect_uri, nonce=nonce)

@app.route("/auth")
async def auth(request: Request):
    try:
        logger.info("Starting Google OAuth authorization process.")
        token = await oauth.google.authorize_access_token(request)
        logger.info(f"Access token received: {token}")

        nonce = request.session.get("nonce")  # Retrieve the nonce from the session
        if not nonce:
            raise HTTPException(status_code=400, detail="Missing nonce for ID token validation")

        user = await oauth.google.parse_id_token(token, nonce=nonce)
        logger.info(f"User information parsed: {user}")

        session_id = secrets.token_hex(16)
        logger.info(f"Generated session ID: {session_id}")

        redis_client.setex(
            f"session:{session_id}", 3600, json.dumps({
                "id_token": token,
                "access_token": token["access_token"],
                "refresh_token": token.get("refresh_token"),  # Use .get() to avoid KeyError
                "user": user,
            })
        )
        logger.info("Session data stored in Redis.")

        # Redirect to the frontend homepage with a success message
        response = RedirectResponse(url=f"http://localhost:9000/?auth=success")
        response.set_cookie(
            key="session_id",
            value=session_id,
            httponly=True,
            secure=True,
            samesite="Lax",
            max_age=3600,
            expires=3600,
        )
        logger.info("Session cookie set successfully.")
        return response
    except Exception as e:
        logger.error(f"Error during authentication: {e}")
        # Redirect to the frontend with an error message
        return RedirectResponse(url=f"http://localhost:9000/auth-failed")

@app.get("/me")
async def me(request: Request):
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(status_code=401, detail="Missing session ID")
    
    session_data = redis_client.get(f"session:{session_id}")
    if not session_data:
        raise HTTPException(status_code=401, detail="Session expired or invalid")
    
    session = json.loads(session_data)
    return {"user": session["user"]}

@app.get("/logout")
async def logout(request: Request):
    session_id = request.cookies.get("session_id")
    if session_id:
        redis_client.delete(f"session:{session_id}")

    response = RedirectResponse(url="/")
    response.delete_cookie("session_id")
    return response