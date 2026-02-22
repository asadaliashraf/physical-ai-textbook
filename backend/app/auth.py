from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr
import uuid
import json

from app.config import settings
from app.database import get_pool

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# ==================
# Pydantic Models
# ==================

class UserBackground(BaseModel):
    programming_experience: str = "none"
    robotics_experience: str = "none"
    hardware_access: str = "none"
    learning_goal: str = "overview"
    preferred_language: str = "english"

class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str
    background: UserBackground = UserBackground()

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict

# ==================
# Helper Functions
# ==================

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    pool = await get_pool()
    async with pool.acquire() as conn:
        user = await conn.fetchrow(
            "SELECT id, email, name, background, preferences FROM users WHERE id = $1",
            uuid.UUID(user_id)
        )
        if not user:
            raise credentials_exception
        result = dict(user)
        if isinstance(result.get("background"), str):
            result["background"] = json.loads(result["background"])
        return result

# ==================
# Auth Routes
# ==================

from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

@auth_router.post("/register", response_model=TokenResponse)
async def register(user_data: UserCreate):
    pool = await get_pool()
    async with pool.acquire() as conn:
        existing = await conn.fetchrow("SELECT id FROM users WHERE email = $1", user_data.email)
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

        hashed_pw = hash_password(user_data.password)
        background_json = json.dumps(user_data.background.model_dump())
        user_id = await conn.fetchval(
            """INSERT INTO users (email, name, hashed_password, background)
               VALUES ($1, $2, $3, $4::jsonb) RETURNING id""",
            user_data.email, user_data.name, hashed_pw, background_json
        )

        access_token = create_access_token({"sub": str(user_id)})
        return TokenResponse(
            access_token=access_token,
            user={"id": str(user_id), "email": user_data.email, "name": user_data.name,
                  "background": user_data.background.model_dump()}
        )

@auth_router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    pool = await get_pool()
    async with pool.acquire() as conn:
        user = await conn.fetchrow("SELECT * FROM users WHERE email = $1", credentials.email)
        if not user or not verify_password(credentials.password, user["hashed_password"]):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

        access_token = create_access_token({"sub": str(user["id"])})
        background = user["background"]
        if isinstance(background, str):
            background = json.loads(background)
        return TokenResponse(
            access_token=access_token,
            user={"id": str(user["id"]), "email": user["email"], "name": user["name"], "background": background}
        )

@auth_router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    return current_user

@auth_router.put("/background")
async def update_background(background: UserBackground, current_user: dict = Depends(get_current_user)):
    pool = await get_pool()
    async with pool.acquire() as conn:
        import json
        await conn.execute(
            "UPDATE users SET background = $1::jsonb, updated_at = NOW() WHERE id = $2",
            json.dumps(background.model_dump()), current_user["id"]
        )
    return {"message": "Background updated successfully"}
