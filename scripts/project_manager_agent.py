import os
from datetime import datetime
import google.generativeai as genai

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise RuntimeError("GOOGLE_API_KEY not set in env or .env file")

genai.configure(api_key=api_key)

with open("scripts/project_manager_agent_prompt.txt") as f:
    prompt = f.read()

readme = open("README.md").read() if os.path.exists("README.md") else ""
build_log = open("build.log").read() if os.path.exists("build.log") else ""

context = f"""
# README
{readme}

# Build Log
{build_log}
"""

full_input = f"{prompt}\n\nContext:\n{context}"

model = genai.GenerativeModel("gemini-pro")
response = model.generate_content(full_input)

os.makedirs("logs", exist_ok=True)
out_path = f"logs/status_{datetime.today().strftime('%Y%m%d')}.md"
with open(out_path, "w") as out:
    out.write(response.text)

print(f"✅ Report written to {out_path}")