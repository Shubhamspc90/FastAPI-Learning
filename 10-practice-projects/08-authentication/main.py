
import hashlib
import hmac
import secrets

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field


app = FastAPI(
    title="Simple Authentication API",
    description="A practice API for user registration, login, and protected routes",
    version="1.0.0",
)


# Authentication configuration
PASSWORD_ITERATIONS = 310_000
bearer_scheme = HTTPBearer(auto_error=False)


# Request and response models
class UserRegister(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: str = Field(
        min_length=5,
        max_length=254,
        pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
    )
    password: str = Field(min_length=8, max_length=128)


class UserLogin(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=128)


class UserProfileUpdate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: str = Field(
        min_length=5,
        max_length=254,
        pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
    )


class UserResponse(BaseModel):
    id: int
    username: str
    email: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str


# In-memory storage. Data resets when the application restarts.
users: list[dict] = []
active_tokens: dict[str, int] = {}


def hash_password(password: str, salt: bytes) -> str:
    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        PASSWORD_ITERATIONS,
    )

    return password_hash.hex()


def verify_password(
    plain_password: str,
    salt: bytes,
    stored_hash: str,
) -> bool:
    calculated_hash = hash_password(plain_password, salt)

    return hmac.compare_digest(calculated_hash, stored_hash)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
):
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials
    user_id = active_tokens.get(token)

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    for user in users:
        if user["id"] == user_id:
            return user

    # The token is no longer valid if its user does not exist.
    active_tokens.pop(token, None)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User associated with this token was not found",
        headers={"WWW-Authenticate": "Bearer"},
    )


@app.post(
    "/auth/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(user: UserRegister):
    normalized_username = user.username.strip().lower()
    normalized_email = user.email.strip().lower()

    if any(
        existing["username"].lower() == normalized_username
        for existing in users
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        )

    if any(
        existing["email"].lower() == normalized_email
        for existing in users
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    salt = secrets.token_bytes(16)
    password_hash = hash_password(user.password, salt)

    new_id = max(
        (existing["id"] for existing in users),
        default=0,
    ) + 1

    new_user = {
        "id": new_id,
        "username": user.username.strip(),
        "email": normalized_email,
        "salt": salt,
        "password_hash": password_hash,
    }

    users.append(new_user)

    return new_user


@app.post("/auth/login", response_model=LoginResponse)
def login_user(credentials: UserLogin):
    normalized_username = credentials.username.strip().lower()

    user = next(
        (
            existing for existing in users
            if existing["username"].lower() == normalized_username
        ),
        None,
    )

    if user is None or not verify_password(
        credentials.password,
        user["salt"],
        user["password_hash"],
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = secrets.token_urlsafe(32)
    active_tokens[access_token] = user["id"]

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@app.get("/auth/me", response_model=UserResponse)
def get_my_profile(current_user: dict = Depends(get_current_user)):
    return current_user


@app.put("/auth/me", response_model=UserResponse)
def update_my_profile(
    updated_profile: UserProfileUpdate,
    current_user: dict = Depends(get_current_user),
):
    normalized_username = updated_profile.username.strip().lower()
    normalized_email = updated_profile.email.strip().lower()

    for existing in users:
        if existing["id"] == current_user["id"]:
            continue

        if existing["username"].lower() == normalized_username:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already exists",
            )

        if existing["email"].lower() == normalized_email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )

    current_user["username"] = updated_profile.username.strip()
    current_user["email"] = normalized_email

    return current_user


@app.post("/auth/logout")
def logout_user(
    current_user: dict = Depends(get_current_user),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    token = credentials.credentials
    active_tokens.pop(token, None)

    return {
        "message": "Logout successful",
        "user_id": current_user["id"],
    }


# cd 10-practice-projects\08-authentication
# uvicorn main:app --reload