from fastapi import APIRouter, Request, Form, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
import json

router = APIRouter(prefix="/auth", tags=["authentication"])
templates = Jinja2Templates(directory="templates")

# Mock user database - in a real app, this would be a database
USERS = {
    "admin@example.com": {
        "email": "admin@example.com",
        "password": "admin",  # In a real app, this would be hashed
        "full_name": "Admin User"
    }
}


class User(BaseModel):
    email: str
    full_name: Optional[str] = None


class UserInDB(User):
    password: str


# Mock authentication - in a real app, use proper authentication
def get_current_user(request: Request):
    user_email = request.session.get("user")
    if not user_email:
        return None
    return User(email=user_email, full_name=USERS.get(user_email, {}).get("full_name"))


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.post("/login")
async def login(
        request: Request,
        email: str = Form(...),
        password: str = Form(...)
):
    user = USERS.get(email)
    if not user or user["password"] != password:
        return templates.TemplateResponse(
            "auth/login.html",
            {"request": request, "error": "Неверный email или пароль"}
        )

    # In a real app, set a secure session cookie
    request.session["user"] = email
    return RedirectResponse(url="/campaigns", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/logout")
async def logout(request: Request):
    request.session.pop("user", None)
    return RedirectResponse(url="/auth/login")


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})


@router.post("/register")
async def register(
        request: Request,
        email: str = Form(...),
        password: str = Form(...),
        full_name: str = Form(...)
):
    if email in USERS:
        return templates.TemplateResponse(
            "auth/register.html",
            {"request": request, "error": "Email уже зарегистрирован"}
        )

    USERS[email] = {
        "email": email,
        "password": password,  # In a real app, this would be hashed
        "full_name": full_name
    }

    # Auto-login after registration
    request.session["user"] = email
    return RedirectResponse(url="/campaigns", status_code=status.HTTP_303_SEE_OTHER)

