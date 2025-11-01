from fastapi import FastAPI, Depends, HTTPException, status, Response, Request, Header
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
import sys
from typing import Optional

sys.path.append(str(Path(__file__).resolve().parents[1]))
import auth as auth_module

app = FastAPI()

# CORS (adjust origins for your frontend dev server)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


class UserCreate(BaseModel):
    username: str
    password: str


@app.on_event("startup")
def startup_event():
    # ensure DB + tables exist
    auth_module.init_db()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/register")
def register(user: UserCreate):
    try:
        auth_module.create_user(user.username, user.password)
    except ValueError:
        raise HTTPException(status_code=400, detail="user already exists")
    return {"msg": "user created"}


@app.post("/token")
def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth_module.get_user(form_data.username)
    if not user or not auth_module.verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = auth_module.create_access_token({"sub": user["username"]})
    # set cookie on the response provided by FastAPI
    response.set_cookie(
        key="session",
        value=access_token,
        httponly=True,
        samesite="lax",
        # secure=True,  # enable in production behind HTTPS
    )
    return {"access_token": access_token, "token_type": "bearer"}


def _resolve_token(request: Request, authorization: Optional[str]) -> Optional[str]:
    # Prefer cookie, fall back to Authorization: Bearer
    cookie_token = request.cookies.get("session")
    if cookie_token:
        return cookie_token
    if authorization and authorization.lower().startswith("bearer "):
        return authorization.split(" ", 1)[1]
    return None


def get_current_user(request: Request, authorization: Optional[str] = Header(default=None)):
    token = _resolve_token(request, authorization)
    if not token:
        raise HTTPException(status_code=401, detail="Missing authentication")
    payload = auth_module.decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    username = payload.get("sub")
    user = auth_module.get_user(username)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user


@app.get("/me")
def read_me(user: dict = Depends(get_current_user)):
    return {"username": user["username"], "created_at": user["created_at"]}


@app.post("/logout")
def logout(response: Response):
    response.delete_cookie("session")
    return {"msg": "logged out"}

