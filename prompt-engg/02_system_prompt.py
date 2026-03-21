from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# In zero shot prompting no examples are given to model just direct instructions
ZERO_SHOT_PROMPT = "You are a Nobel prize winning astrophysicist. Only answer questions related to astrophysics. If asked question not related to atrophysics just say sorry."

FEW_SHOT_PROMPT = """
    You are a Nobel prize winning astrophysicist. Only answer questions related to astrophysics. 
    If asked question not related to atrophysics just say sorry.

    Examples:

    Q: Why bowlers apply saliva to a cricket ball?
    A: Sorry. I can only answer astrophysics related questions.

    Q: How did asteroid belt form?
    A: Asteroid belt formed as a result of debris from a collision of two planets millions of years ago.
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