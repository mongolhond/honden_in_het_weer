import os
import datetime
from google import genai

# Initialize the Gemini client (reads your GEMINI_API_KEY secret automatically)
client = genai.Client()

# Define the instruction prompt for Gemini
prompt = (
    "Generate a structured daily handoff log template in Markdown format. "
    "Include sections for Objectives, Key Progress, Constraints, and Open Questions."
)

# Call Gemini model using current stable Flash model
response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=prompt,
)

# Create a timestamp and ensure the destination directory exists
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
os.makedirs("logs", exist_ok=True)
filename = f"logs/snapshot_{timestamp}.md"

# Save response content to a Markdown file
with open(filename, "w", encoding="utf-8") as f:
    f.write(f"# Automated Session Snapshot ({timestamp})\n\n")
    f.write(response.text)

print(f"Snapshot created successfully: {filename}")
