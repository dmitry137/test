from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.security import OAuth2PasswordRequestForm
import uvicorn
from pathlib import Path

# Import routers
from routers import auth, campaigns, uploads


app = FastAPI(title="Campaign Management System",
    middleware=[
        Middleware(SessionMiddleware, secret_key="bXF2cU1zR21tNzJtY0t3WURpTXl6T2hVMHRqRXh0VlBqU1FFeUp5RjQ=")
    ]
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Include routers
app.include_router(auth.router)
app.include_router(campaigns.router)
app.include_router(uploads.router)

@app.get("/")
async def root(request: Request):
    # Redirect to login page
    return RedirectResponse(url="/auth/login")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=6000, reload=True)

