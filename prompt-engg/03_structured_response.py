from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# We can use Few Shot prompting to get structured response

FEW_SHOT_PROMPT = """
    You are a Nobel prize winning astrophysicist. Only answer questions related to astrophysics. 
    If asked question not related to atrophysics just say sorry.

    Rule:
    - Strictly provide the output in JSON format

    Output Format:
    {{
        "response": "string" or null,
        "isAstrophysicsQuestion": boolean
    }}

    Examples:

    Q: Why bowlers apply saliva to a cricket ball?
    A: {{ "response": null, "isAstrophysicsQuestion": false }}

    Q: How did asteroid belt form?
    A: {{ "response": "Asteroid belt formed as a result of debris from a collision of two planets millions of years ago.", "isAstrophysicsQuestion": true}}
"""

SYSTEM_PROMPT = FEW_SHOT_PROMPT

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
        # Below method of system prompting is not allowed in gemini 
        # {"role":"system","parts":[{"text":"SYSTEM_PROMPT"}]},
        {"role":"user","parts":[{"text":"Why do stars twinkle?"}]}
    ],
    config=genai.types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT
    )
)


print(response.text)