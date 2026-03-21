from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[
        {"role":"user","parts":[{"text":"tell me a joke"}]}
    ]
)
print(response.text)
print(response)