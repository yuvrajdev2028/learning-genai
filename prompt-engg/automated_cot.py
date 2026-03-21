from google import genai
import os
from dotenv import load_dotenv
import json
import time

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Chain of thought prompting involves letting the model to list out the way it is thinking and acting to get a solution to the user query
#  Here we are automating this process

CHAIN_OF_THOUGHT_PROMPT = """
    You are an expert AI assistant that can easily resolve user queries using chain of thought.
    You work on START,PLAN and OUTPUT steps.
    You need to forst PLAN what needs to be done. PLAN can be in multiple steps. The final step is OUTPUT.
    Once enpught planning is done you can provide the OUTPUT.

    Rule:
    - Strictly provide the output in JSON format
    - Only run and provide one step at a time
    - The sequence of steps is START where user provides query, the PLAN steps (use multiple PLAN steps) where you tell what you are thinking of, 
    and then finally OUTPUT step where you provide the final output

    IMPORTANT: You must only output exactly ONE JSON object per response. Do not generate a list of objects. 
    After outputting the closing brace '}', stop immediately.

    Output JSON Format:
    {
        "step": "START" | "PLAN" | "OUTPUT",
        "content" : "string"
    }

    Examples:

    START: Solve 2*3+8/2
    PLAN: { "step": "PLAN", "content": "User wants to solve 2*3+8/2"}
    PLAN: { "step": "PLAN", "content": "This seems to be a arithmetic problem where we can use BODMAS rule"}
    PLAN: { "step": "PLAN", "content": "Solving given problem using BODMAS..."}
    OUTPUT: { "step": "OUTPUT", "content": "8/2 = 4, 2*3 = 6, 4+6 = 10, So the answer is 10.}
"""

SYSTEM_PROMPT = CHAIN_OF_THOUGHT_PROMPT

chat_history = []

while True:

    initial_prompt = input('->')
    chat_history.append({"role":"user","parts":[{"text":initial_prompt}]})


    while True:
        response = client.models.generate_content(
            model='gemini-3.1-flash-lite-preview',
            contents=chat_history,
            config = genai.types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                response_mime_type="application/json", # Use this to force Gemini to always provide json output.
                stop_sequences=["}"] #Use this to ensure that model stops talking the moment first JSON object is returned
            )
        )

        # this can evaluate to None based on output format
        # response structure can be like this as well -> response.candidates[0].content.parts[0].text
        # So it is best we handle this
        # output = json.loads(response.text) 

        text = response.text.strip()

        if not text:
            print("Model returned empty response")
            break

        # This is to ensure that if model cuts last character due to stop sequences we can ensure valid JSON structure
        if not text.endswith("}"):
            text += "}"

        try:
            output = json.loads(text)
            step_type = output.get("step")
            content = output.get("content")
            
            print(f"[{step_type}]: {content}")

            chat_history.append({
                "role": "model",
                "parts": [{"text": json.dumps(output)}]
            })

            if step_type == "OUTPUT":
                break

            time.sleep(0.8)
        except json.JSONDecodeError:
            print(f"Error parsing JSON. Raw output: {text}")
            break

    print("\n")
