from fastapi import FastAPI, Header, HTTPException

app = FastAPI(title="Secure-SRE API")

@app.get("/health")
def health_check():
    # SRE: Basic endpoint for uptime monitoring
    return {"status": "healthy", "version": "1.0.0"}

@app.get("/secure-data")
def get_data(x_api_key: str = Header(None)):
    # Security: Simple header-based protection
    if x_api_key != "secret-key-123":
        raise HTTPException(status_code=403, detail="Unauthorized")
    return {"data": "This is protected info"}