import os
import datetime
import time
from google import genai
from google.genai.errors import ServerError

# Initialize the Gemini client
client = genai.Client()

prompt = (
    "Generate a structured daily handoff log template in Markdown format. "
    "Include sections for Objectives, Key Progress, Constraints, and Open Questions."
)

# Active Gemini 3.x model identifiers
models_to_try = ["gemini-3.8-flash", "gemini-3.5-flash-lite", "gemini-3.6-flash"]
response = None

for model in models_to_try:
    for attempt in range(3):
        try:
            print(f"Attempting request using model: '{model}' (Attempt {attempt + 1})...")
            response = client.models.generate_content(
                model=model,
                contents=prompt,
            )
            print(f"Successfully generated response using '{model}'.")
            break
        except ServerError:
            print(f"Google API reported high demand on '{model}'. Retrying in 5 seconds...")
            time.sleep(5)
        except Exception as e:
            print(f"Could not connect to model '{model}': {e}")
            break
            
    if response:
        break

if not response:
    raise RuntimeError("Unable to reach active Gemini API models. Please verify API key and permissions.")

# Create timestamp and output directory
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
os.makedirs("logs", exist_ok=True)
filename = f"logs/snapshot_{timestamp}.md"

# Save response content to Markdown
with open(filename, "w", encoding="utf-8") as f:
    f.write(f"# Automated Session Snapshot ({timestamp})\n\n")
    f.write(response.text)

print(f"Snapshot saved successfully to {filename}")
