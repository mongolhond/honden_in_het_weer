import os
import datetime
from google import genai

client = genai.Client()

# Retrieve the pasted chat content from GitHub Actions
user_input = os.environ.get("USER_CHAT_INPUT", "No chat content provided.")

prompt = f"""
Summarize the following chat log into a structured handoff document in Markdown format.
Include Objectives, Key Progress, Constraints, and Open Questions based strictly on this text:

---
{user_input}
---
"""

response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=prompt,
)

timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
os.makedirs("logs", exist_ok=True)
filename = f"logs/snapshot_{timestamp}.md"

with open(filename, "w", encoding="utf-8") as f:
    f.write(f"# Session Snapshot ({timestamp})\n\n")
    f.write(response.text)

print(f"Snapshot saved to {filename}")
