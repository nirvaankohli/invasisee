from fastapi import FastAPI, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
import auth as auth_module

app = FastAPI()

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
    response.set_cookie(key="session", value=access_token, httponly=True, samesite="lax")
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/me")
def read_me(token: str = Depends(oauth2_scheme)):
    payload = auth_module.decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    username = payload.get("sub")
    user = auth_module.get_user(username)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return {"username": user["username"], "created_at": user["created_at"]}

