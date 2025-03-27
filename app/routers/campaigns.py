from fastapi import APIRouter, Request, Form, Depends, HTTPException, status, Path
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict
import json
from datetime import datetime

from routers.auth import get_current_user, User

router = APIRouter(tags=["campaigns"])
templates = Jinja2Templates(directory="templates")

# Mock campaign database - in a real app, this would be a database
CAMPAIGNS = {
    "1": {
        "id": "1",
        "name": "Christmas Campaign 2024",
        "status": "stopped",
        "created_at": "2024-03-27T12:00:00",
        "settings": {
            "email": {
                "password_mail": "app_password_123",
                "sender_mail": "sender@example.com",
                "receiver_mail": "receiver1@example.com, receiver2@example.com",
                "subject": "Christmas Greetings"
            },
            "telegram": {
                "bot_token": "1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                "target_chat_id": "-1001234567890",
                "file_order": "image1.jpg, image2.jpg"
            },
            "s3": {
                "send_timeout": 30,
                "delay_send": 5
            }
        },
        "recipients": [
            {"name": "John Doe", "email": "john@example.com", "description": "VIP Customer"},
            {"name": "Jane Smith", "email": "jane@example.com", "description": "Regular Customer"}
        ],
        "email_template": "Dear {{name}},\n\nMerry Christmas and Happy New Year!\n\nBest regards,\nThe Team",
        "telegram_template": "🎄 Merry Christmas and Happy New Year! 🎄"
    },
    "2": {
        "id": "2",
        "name": "New Year Campaign 2025",
        "status": "running",
        "created_at": "2024-03-27T14:30:00",
        "settings": {
            "email": {
                "password_mail": "app_password_456",
                "sender_mail": "sender@example.com",
                "receiver_mail": "receiver3@example.com, receiver4@example.com",
                "subject": "New Year Greetings"
            },
            "telegram": {
                "bot_token": "0987654321:ZYXWVUTSRQPONMLKJIHGFEDCBA",
                "target_chat_id": "-1009876543210",
                "file_order": "newyear1.jpg, newyear2.jpg"
            },
            "s3": {
                "send_timeout": 20,
                "delay_send": 3
            }
        },
        "recipients": [
            {"name": "Alice Johnson", "email": "alice@example.com", "description": "New Customer"},
            {"name": "Bob Brown", "email": "bob@example.com", "description": "Premium Customer"}
        ],
        "email_template": "Dear {{name}},\n\nHappy New Year 2025!\n\nBest regards,\nThe Team",
        "telegram_template": "🎉 Happy New Year 2025! 🎉"
    }
}

# Mock templates and recipient lists
EMAIL_TEMPLATES = {
    "christmas": "Dear {{name}},\n\nMerry Christmas and Happy New Year!\n\nBest regards,\nThe Team",
    "new_year": "Dear {{name}},\n\nHappy New Year 2025!\n\nBest regards,\nThe Team",
    "birthday": "Dear {{name}},\n\nHappy Birthday!\n\nBest regards,\nThe Team"
}

TELEGRAM_TEMPLATES = {
    "christmas": "🎄 Merry Christmas and Happy New Year! 🎄",
    "new_year": "🎉 Happy New Year 2025! 🎉",
    "birthday": "🎂 Happy Birthday! 🎂"
}

RECIPIENT_LISTS = {
    "vip": [
        {"name": "John Doe", "email": "john@example.com", "description": "VIP Customer"},
        {"name": "Jane Smith", "email": "jane@example.com", "description": "VIP Customer"}
    ],
    "regular": [
        {"name": "Alice Johnson", "email": "alice@example.com", "description": "Regular Customer"},
        {"name": "Bob Brown", "email": "bob@example.com", "description": "Regular Customer"}
    ],
    "new": [
        {"name": "Charlie Wilson", "email": "charlie@example.com", "description": "New Customer"},
        {"name": "Diana Miller", "email": "diana@example.com", "description": "New Customer"}
    ]
}

class CampaignCreate(BaseModel):
    name: str
    email_settings: dict
    telegram_settings: dict
    s3_settings: dict
    recipients: List[dict]
    email_template: str
    telegram_template: str

@router.get("/campaigns", response_class=HTMLResponse)
async def list_campaigns(request: Request, current_user: User = Depends(get_current_user)):
    if not current_user:
        return RedirectResponse(url="/auth/login")
    
    return templates.TemplateResponse(
        "campaigns/list.html", 
        {"request": request, "campaigns": CAMPAIGNS, "user": current_user}
    )

@router.get("/campaigns/create", response_class=HTMLResponse)
async def create_campaign_page(request: Request, current_user: User = Depends(get_current_user)):
    if not current_user:
        return RedirectResponse(url="/auth/login")
    
    return templates.TemplateResponse(
        "campaigns/create.html", 
        {
            "request": request, 
            "user": current_user,
            "email_templates": EMAIL_TEMPLATES,
            "telegram_templates": TELEGRAM_TEMPLATES,
            "recipient_lists": RECIPIENT_LISTS
        }
    )

@router.post("/campaigns/create")
async def create_campaign(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    if not current_user:
        return RedirectResponse(url="/auth/login")
    
    form_data = await request.form()
    
    # Generate a new ID (in a real app, this would be handled by the database)
    new_id = str(len(CAMPAIGNS) + 1)
    
    # Create new campaign
    CAMPAIGNS[new_id] = {
        "id": new_id,
        "name": form_data.get("name"),
        "status": "stopped",
        "created_at": datetime.now().isoformat(),
        "settings": {
            "email": {
                "password_mail": form_data.get("password_mail"),
                "sender_mail": form_data.get("sender_mail"),
                "receiver_mail": form_data.get("receiver_mail"),
                "subject": form_data.get("subject")
            },
            "telegram": {
                "bot_token": form_data.get("bot_token"),
                "target_chat_id": form_data.get("target_chat_id"),
                "file_order": form_data.get("file_order")
            },
            "s3": {
                "send_timeout": int(form_data.get("send_timeout", 30)),
                "delay_send": int(form_data.get("delay_send", 5))
            }
        },
        "recipients": json.loads(form_data.get("recipients", "[]")),
        "email_template": form_data.get("email_template"),
        "telegram_template": form_data.get("telegram_template")
    }
    
    return RedirectResponse(url="/campaigns", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/campaigns/{campaign_id}/edit", response_class=HTMLResponse)
async def edit_campaign_page(
    request: Request, 
    campaign_id: str = Path(...),
    current_user: User = Depends(get_current_user)
):
    if not current_user:
        return RedirectResponse(url="/auth/login")
    
    campaign = CAMPAIGNS.get(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    return templates.TemplateResponse(
        "campaigns/edit.html", 
        {
            "request": request, 
            "user": current_user,
            "campaign": campaign,
            "email_templates": EMAIL_TEMPLATES,
            "telegram_templates": TELEGRAM_TEMPLATES,
            "recipient_lists": RECIPIENT_LISTS
        }
    )

@router.post("/campaigns/{campaign_id}/edit")
async def edit_campaign(
    request: Request,
    campaign_id: str = Path(...),
    current_user: User = Depends(get_current_user)
):
    if not current_user:
        return RedirectResponse(url="/auth/login")
    
    campaign = CAMPAIGNS.get(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    form_data = await request.form()
    print(form_data)
    # Update campaign
    CAMPAIGNS[campaign_id] = {
        "id": campaign_id,
        "name": form_data.get("name"),
        "status": campaign["status"],
        "created_at": campaign["created_at"],
        "settings": {
            "email": {
                "password_mail": form_data.get("password_mail"),
                "sender_mail": form_data.get("sender_mail"),
                "receiver_mail": form_data.get("receiver_mail"),
                "subject": form_data.get("subject")
            },
            "telegram": {
                "bot_token": form_data.get("bot_token"),
                "target_chat_id": form_data.get("target_chat_id"),
                "file_order": form_data.get("file_order")
            },
            "s3": {
                "send_timeout": int(form_data.get("send_timeout", 30)),
                "delay_send": int(form_data.get("delay_send", 5))
            }
        },
        "recipients": json.loads(form_data.get("recipients", "[]")),
        "email_template": form_data.get("email_template"),
        "telegram_template": form_data.get("telegram_template")
    }
    
    return RedirectResponse(url="/campaigns", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/campaigns/{campaign_id}/toggle")
async def toggle_campaign(
    campaign_id: str = Path(...),
    current_user: User = Depends(get_current_user)
):
    if not current_user:
        return JSONResponse({"error": "Not authenticated"}, status_code=401)
    
    campaign = CAMPAIGNS.get(campaign_id)
    if not campaign:
        return JSONResponse({"error": "Campaign not found"}, status_code=404)
    
    # Toggle status
    new_status = "stopped" if campaign["status"] == "running" else "running"
    CAMPAIGNS[campaign_id]["status"] = new_status
    
    return JSONResponse({"status": new_status})

