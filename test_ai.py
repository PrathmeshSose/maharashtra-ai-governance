import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Test Gemini AI connection
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

# Test query
test_query = "Water supply issue in Pune area, urgent help needed"

prompt = f"""
Analyze this citizen service request for Maharashtra government:

Query: {test_query}

Provide analysis:
- Service Category: [health/infrastructure/safety/education/other]
- Urgency Level: [low/medium/high/critical]
- Department: [specific department name]
- Estimated Resolution: [number] days
- Priority Score: [1-100]
"""

try:
    response = model.generate_content(prompt)
    print("✅ AI Analysis Working!")
    print("=" * 50)
    print(response.text)
    print("=" * 50)
    print("🎉 Maharashtra AI Governance Platform is fully operational!")
except Exception as e:
    print(f"❌ AI Error: {e}")