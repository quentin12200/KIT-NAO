"""Web routes for HTML pages."""
from fastapi import APIRouter, Request, Depends, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import timedelta

from app.database import get_db
from app.models.user import User
from app.utils.auth import verify_password, create_access_token, get_current_active_user
from app.config import settings
import os

router = APIRouter()

# Setup templates
templates_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates", "web")
templates = Jinja2Templates(directory=templates_dir)


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page."""
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, registered: str = None):
    """Login page."""
    context = {"request": request}
    if registered:
        context["success"] = "Inscription réussie ! Vous pouvez maintenant vous connecter."
    return templates.TemplateResponse("login.html", context)


@router.post("/login")
async def login_submit(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """Handle login form submission."""
    # Find user by email
    user = db.query(User).filter(User.email == username).first()

    # Verify credentials
    if not user or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Email ou mot de passe incorrect"},
            status_code=400
        )

    # Check if user is active
    if not user.is_active:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Compte désactivé"},
            status_code=400
        )

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"user_id": user.id, "email": user.email}, expires_delta=access_token_expires
    )

    # Redirect to dashboard with token in cookie
    response = RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax"
    )
    return response


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Registration page."""
    return templates.TemplateResponse("register.html", {"request": request})


@router.get("/logout")
async def logout():
    """Logout user."""
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie(key="access_token")
    return response


# Helper function to get current user from cookie
async def get_current_user_optional(request: Request, db: Session = Depends(get_db)):
    """Get current user from cookie, return None if not authenticated."""
    try:
        token = request.cookies.get("access_token")
        if not token:
            return None

        # Remove "Bearer " prefix if present
        if token.startswith("Bearer "):
            token = token[7:]

        from app.utils.auth import decode_access_token
        token_data = decode_access_token(token)
        if token_data is None or token_data.user_id is None:
            return None

        user = db.query(User).filter(User.id == token_data.user_id).first()
        if user and user.is_active:
            return user
        return None
    except Exception:
        return None


async def get_current_user_required(request: Request, db: Session = Depends(get_db)):
    """Get current user from cookie, redirect to login if not authenticated."""
    user = await get_current_user_optional(request, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail="Not authenticated",
            headers={"Location": "/login"}
        )
    return user


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    db: Session = Depends(get_db)
):
    """Dashboard page (protected)."""
    user = await get_current_user_optional(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    # Get counts for stats
    from app.models.campaign import Campaign
    from app.models.document import Document
    from app.models.organization import Organization

    campaigns_count = db.query(Campaign).count()
    documents_count = db.query(Document).count()
    organizations_count = db.query(Organization).count()

    # Get recent campaigns
    campaigns = db.query(Campaign).order_by(Campaign.created_at.desc()).limit(5).all()

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "user": user,
            "campaigns_count": campaigns_count,
            "documents_count": documents_count,
            "organizations_count": organizations_count,
            "campaigns": campaigns
        }
    )
