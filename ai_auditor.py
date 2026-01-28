import os
import google.generativeai as genai
from dotenv import load_dotenv  # <-- Important: This reads your .env file
import boto3
from datetime import datetime

# 1. Initialize: This pulls your secrets into the script
load_dotenv(override=True)
api_key = os.getenv("GEMINI_API_KEY")

# 2. Configure the "Brain"
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-flash-latest')

def analyze_logs_with_ai(log_data: str):
    # This is the "Prompt" - how we talk to the AI
    prompt = f"""
    You are an expert DevSecOps Engineer. Analyze the following application logs 
    for security threats (like SQL injection or Brute Force) and SRE performance 
    issues (like latency spikes).
    
    LOGS:
    {log_data}
    
    Return a response with:
    1. 'threat_level': (Low/Medium/High)
    2. 'summary': Short description of findings.
    3. 'recommendation': What the engineer should do.
    """
    response = model.generate_content(prompt)
    return response.text


# ... (Logs uploading to Cloud function)

def save_audit_to_s3(report_text: str, bucket_name: str):
    """
    Saves the AI analysis report to our secure S3 bucket with AES256 encryption.
    """
    s3 = boto3.client('s3')
    
    # Generate a unique filename using the current date and time
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"audit_logs/report_{timestamp}.txt"
    
    try:
        s3.put_object(
            Bucket=bucket_name,
            Key=filename,
            Body=report_text,
            ServerSideEncryption='AES256'  # Rank 1: Security Requirement
        )
        print(f"🚀 [SRE] Report successfully vaulted to S3: {filename}")
    except Exception as e:
        print(f"⚠️ [SRE Error] Failed to upload to cloud: {e}")



# --- QUICK TEST BLOCK ---
if __name__ == "__main__":

    # 1. Simulate a report

    fake_logs = """
    2026-01-22 10:01:01 - INFO - User 'admin' failed login - IP 192.168.1.50
    2026-01-22 10:01:02 - INFO - User 'admin' failed login - IP 192.168.1.50
    2026-01-22 10:01:03 - INFO - User 'admin' failed login - IP 192.168.1.50
    2026-01-22 10:01:04 - INFO - User 'admin' failed login - IP 192.168.1.50
    """

    # 2. Use YOUR bucket name from the Terraform output or AWS Console
    MY_BUCKET_NAME = "secure-sre-logs-41b3e3c1"

    print("--- SRE AI Auditor is scanning logs ---")
    analysis_report = analyze_logs_with_ai(fake_logs)
    print(analysis_report)

    print("\n--- ☁️ Step 2: Vaulting Report to AWS ---")
    save_audit_to_s3(analysis_report, MY_BUCKET_NAME)