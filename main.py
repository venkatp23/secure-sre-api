from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from auth import create_access_token, verify_password, hash_password
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from ai_auditor import analyze_logs_with_ai


templates = Jinja2Templates(directory="templates")

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/health")
async def health_check():
    # This returns a simple JSON 'OK' to Docker's healthcheck
    return {"status": "healthy"}

# Mock Database for Day 2
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "hashed_password": hash_password("Choose-A-Strong-Service-Password-2026"),
    }
}

@app.get("/", response_class=HTMLResponse)
async def read_login(request: Request):
    # This serves the HTML file we just created
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/secure-data")
async def get_secure_data(token: str = Depends(oauth2_scheme)):
    # This endpoint is now protected by a JWT gate!
    return {"message": "SRE Reliability Tip: Always rotate your secrets!"}

@app.post("/sre/audit")
async def run_ai_audit(logs: str, token: str = Depends(oauth2_scheme)):
    """
    This endpoint allows an SRE to paste logs and get an 
    immediate AI security and performance report.
    """
    # 1. We take the logs provided by the user
    # 2. We send them to our Gemini 'Brain'
    analysis = analyze_logs_with_ai(logs)
    
    # 3. We return the AI's wisdom
    return {"ai_analysis": analysis}