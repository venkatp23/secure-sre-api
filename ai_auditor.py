import os
import time
import boto3
from datetime import datetime
from google.genai import Client
from google.genai.errors import ClientError
from dotenv import load_dotenv

load_dotenv(override=True)

def analyze_logs_with_ai(log_data: str):
    # SRE Best Practice: Get the key and init client INSIDE the function
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        # Instead of crashing, we return a helpful SRE message
        return "Error: GEMINI_API_KEY not found in environment."

    client = Client(api_key=api_key)
    
    prompt = f"""
    Analyze these logs for security threats and SRE performance issues.
    LOGS: {log_data}
    """
    
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model='gemini-2.0-flash', # Correcting to the standard flash model name
                contents=prompt
            )
            return response.text
        except ClientError as e:
            if "429" in str(e) and attempt < 2:
                time.sleep(60)
                continue
            # If we hit the 20-request limit, we handle it gracefully
            return f"AI Audit failed: {str(e)}"