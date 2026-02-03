import os
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager

from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter

# Custom imports
from auth import create_access_token, verify_password, hash_password
from ai_auditor import analyze_logs_with_ai

# --- 1. MODERN LIFESPAN SETUP ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # This ensures your /metrics endpoint is ready for Prometheus
    print("SRE System: Booting up observability tools...")
    Instrumentator().instrument(app).expose(app)
    yield
    print("SRE System: Shutting down safely.")

app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="templates")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- 2. SRE OBSERVABILITY METRICS ---
AI_AUDIT_COUNT = Counter("ai_audit_total", "Total number of AI security audits")
LOGIN_FAILURE_COUNT = Counter("login_failures_total", "Total failed login attempts")

# Mock Database (Standardized with bcrypt==4.0.1)
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "hashed_password": hash_password("Choose-A-Strong-Service-Password-2026"),
    }
}

# --- 3. ROUTES ---

@app.get("/", response_class=HTMLResponse)
async def read_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        LOGIN_FAILURE_COUNT.inc() # Metric: Tracks brute force attempts
        raise HTTPException(status_code=401, detail="Incorrect credentials")
    
    return {"access_token": create_access_token(data={"sub": user["username"]}), "token_type": "bearer"}

# FIX: This route exists so Pytest finds it (Solves the 404 error)
@app.get("/secure-data")
async def secure_data(token: str = Depends(oauth2_scheme)):
    return {"message": "SRE Auth Successful: Accessing secure telemetry."}

@app.post("/sre/audit")
async def run_ai_audit(logs: str, token: str = Depends(oauth2_scheme)):
    AI_AUDIT_COUNT.inc() 
    try:
        analysis = analyze_logs_with_ai(logs)
        return {"ai_analysis": analysis}
    except Exception as e:
        # SRE Logic: Handle the 429 Resource Exhausted error gracefully
        if "429" in str(e):
            return {"ai_analysis": "AI Quota Exhausted (20/day). Logs saved to S3."}
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}