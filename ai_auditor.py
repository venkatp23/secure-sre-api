import os
import google.generativeai as genai
from dotenv import load_dotenv  # <-- Important: This reads your .env file

# 1. Initialize: This pulls your secrets into the script
load_dotenv()
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

def auto_remediate(analysis_text: str):
    if "High" in analysis_text or "Critical" in analysis_text:
        print("🚨 AUTO-HEALER TRIGGERED!")
        print("ACTION: Restarting Database Service... (Simulated)")
        print("ACTION: Blocking Malicious IP... (Simulated)")
    else:
        print("✅ System within normal limits. No auto-action required.")

# 3. The "Test Drive" - simulate a hacker trying a Brute Force attack
if __name__ == "__main__":
    fake_logs = """
    2026-01-22 10:01:01 - INFO - User 'admin' failed login - IP 192.168.1.50
    2026-01-22 10:01:02 - INFO - User 'admin' failed login - IP 192.168.1.50
    2026-01-22 10:01:03 - INFO - User 'admin' failed login - IP 192.168.1.50
    2026-01-22 10:01:04 - INFO - User 'admin' failed login - IP 192.168.1.50
    """
    print("--- SRE AI Auditor is scanning logs ---")
    print(analyze_logs_with_ai(fake_logs))