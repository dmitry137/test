from fastapi import APIRouter, Request, File, UploadFile, Form, Depends, HTTPException
from fastapi.responses import JSONResponse
import csv
import io
from typing import List

from app.routers.auth import get_current_user, User

router = APIRouter(prefix="/uploads", tags=["uploads"])


@router.post("/recipients")
async def upload_recipients(
        request: Request,
        file: UploadFile = File(...),
        list_name: str = Form(...),
        current_user: User = Depends(get_current_user)
):
    if not current_user:
        return JSONResponse({"error": "Not authenticated"}, status_code=401)

    # Process the uploaded file
    content = await file.read()

    # Parse CSV or TXT file
    recipients = []

    if file.filename.endswith('.csv'):
        # Parse CSV
        text = content.decode('utf-8')
        csv_reader = csv.DictReader(io.StringIO(text))
        for row in csv_reader:
            recipients.append({
                "name": row.get("name", ""),
                "email": row.get("email", ""),
                "description": row.get("description", "")
            })
    else:
        # Parse TXT (assuming comma-separated values)
        text = content.decode('utf-8')
        for line in text.splitlines():
            if line.strip():
                parts = line.split(',')
                recipients.append({
                    "name": parts[0].strip() if len(parts) > 0 else "",
                    "email": parts[1].strip() if len(parts) > 1 else "",
                    "description": parts[2].strip() if len(parts) > 2 else ""
                })

    # In a real app, save to database
    # For now, just return the parsed recipients
    return JSONResponse({
        "success": True,
        "list_name": list_name,
        "recipients": recipients
    })


@router.post("/template")
async def upload_template(
        request: Request,
        file: UploadFile = File(...),
        template_name: str = Form(...),
        template_type: str = Form(...),  # "email" or "telegram"
        current_user: User = Depends(get_current_user)
):
    if not current_user:
        return JSONResponse({"error": "Not authenticated"}, status_code=401)

    # Process the uploaded file
    content = await file.read()
    template_content = content.decode('utf-8')

    # In a real app, save to database
    # For now, just return the template content
    return JSONResponse({
        "success": True,
        "template_name": template_name,
        "template_type": template_type,
        "content": template_content
    })


@router.post("/settings")
async def upload_settings(
        request: Request,
        file: UploadFile = File(...),
        template_name: str = Form(...),
        current_user: User = Depends(get_current_user)
):
    if not current_user:
        return JSONResponse({"error": "Not authenticated"}, status_code=401)

    # Process the uploaded file
    content = await file.read()

    try:
        # Parse settings from file content
        text = content.decode('utf-8')

        # In a real app, you would parse the file content properly
        # For now, just create a simple settings object
        settings = {
            "email": {
                "password_mail": "uploaded_password",
                "sender_mail": "uploaded@example.com",
                "subject": "Uploaded Subject"
            },
            "telegram": {
                "bot_token": "uploaded_token",
                "target_chat_id": "uploaded_chat_id",
                "file_order": "uploaded1.jpg, uploaded2.jpg"
            },
            "s3": {
                "send_timeout": 25,
                "delay_send": 4
            }
        }

        # In a real app, save to database
        return JSONResponse({
            "success": True,
            "template_name": template_name,
            "settings": settings
        })
    except Exception as e:
        return JSONResponse({
            "error": f"Failed to parse settings file: {str(e)}"
        }, status_code=400)

