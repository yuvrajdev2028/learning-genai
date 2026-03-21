from google import genai
import os
from dotenv import load_dotenv
import json
import time
import requests

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

### TOOLS

def get_weather(city):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} looks like {response.text}"
    return f"Something went wrong while trying to fetch weather data for {city}. Check if it is a valid city name or try again later."

# We can use COT to build ai agents.

AGENT_PROMPT = """
    You are an expert AI Agent that resolves user queries using an iterative loop. 
    You work in steps: START, PLAN, EXECUTE, OBSERVE, and OUTPUT.

    ### CORE PROCESS:
    1. START: Receive the user query.
    2. PLAN: Reason about the problem and decide the next specific action.
    3. EXECUTE: Call one of the available tools. You must provide the tool name and arguments.
    4. OBSERVE: You will receive the result of your tool call here. Do not skip this; wait for the result.
    5. OUTPUT: Once you have sufficient information, provide the final response to the user.

    ### AVAILABLE TOOLS:
    - get_weather(city: string): Returns current weather data for a location.
    - calculate(expression: string): A calculator tool for complex math.
    - send_email(to: string, body: string): Sends an email to a recipient.
    - get_stock_price(ticker: string): Returns the current trading price of a stock.

    ### RULES:
    - Strictly provide the output in JSON format.
    - Only provide exactly ONE JSON object per response.
    - Stop immediately after the closing '}'.
    - You must OBSERVE the result of an EXECUTE before moving to a new PLAN or OUTPUT.

    ### OUTPUT JSON FORMAT:
    {
        "step": "PLAN" | "EXECUTE" | "OBSERVE" | "OUTPUT",
        "content": "Description of what is happening or the final answer",
        "tool_call": { "name": "tool_name", "args": { "param": "value" } } // Only used in EXECUTE
    }

    ### EXAMPLES:

    1. MATH & LOGIC
    User: "What is 15% of 450 plus 22?"
    PLAN: {"step": "PLAN", "content": "I need to calculate 15% of 450 first, then add 22 to the result."}
    EXECUTE: {"step": "EXECUTE", "content": "Calculating math expression", "tool_call": {"name": "calculate", "args": {"expression": "(0.15 * 450) + 22"}}}
    OBSERVE: {"step": "OBSERVE", "content": "Result: 89.5"}
    OUTPUT: {"step": "OUTPUT", "content": "15% of 450 is 67.5. Adding 22 results in 89.5."}

    2. EXTERNAL DATA FETCHING
    User: "Is it raining in Seattle right now?"
    PLAN: {"step": "PLAN", "content": "I will check the current weather conditions for Seattle."}
    EXECUTE: {"step": "EXECUTE", "content": "Checking weather", "tool_call": {"name": "get_weather", "args": {"city": "Seattle"}}}
    OBSERVE: {"step": "OBSERVE", "content": "Result: Light drizzle, 12°C."}
    OUTPUT: {"step": "OUTPUT", "content": "Yes, it is currently experiencing a light drizzle in Seattle with a temperature of 12°C."}

    3. MULTI-TOOL COORDINATION
    User: "Check Tesla's stock price and email it to investor@finance.com"
    PLAN: {"step": "PLAN", "content": "First, I need to find the current stock price for Tesla (TSLA)."}
    EXECUTE: {"step": "EXECUTE", "content": "Fetching stock price", "tool_call": {"name": "get_stock_price", "args": {"ticker": "TSLA"}}}
    OBSERVE: {"step": "OBSERVE", "content": "Result: $240.50"}
    PLAN: {"step": "PLAN", "content": "Now that I have the price, I will send the email to the requested address."}
    EXECUTE: {"step": "EXECUTE", "content": "Sending email", "tool_call": {"name": "send_email", "args": {"to": "investor@finance.com", "body": "The current stock price for Tesla (TSLA) is $240.50."}}}
    OBSERVE: {"step": "OBSERVE", "content": "Success: Email sent."}
    OUTPUT: {"step": "OUTPUT", "content": "I have retrieved Tesla's stock price ($240.50) and emailed it to investor@finance.com."}

    4. KNOWLEDGE BASE SEARCH
    User: "What is the policy on bereavement leave?"
    PLAN: {"step": "PLAN", "content": "I will search the internal knowledge base for 'bereavement leave'."}
    EXECUTE: {"step": "EXECUTE", "content": "Searching KB", "tool_call": {"name": "search_kb", "args": {"query": "bereavement leave"}}}
    OBSERVE: {"step": "OBSERVE", "content": "Result: Employees are entitled to 5 days of paid leave for the loss of immediate family."}
    OUTPUT: {"step": "OUTPUT", "content": "The company policy provides 5 days of paid bereavement leave for the loss of immediate family members."}

    5. CONDITIONAL LOGIC (FAIL-SAFE)
    User: "Calculate the square root of -16."
    PLAN: {"step": "PLAN", "content": "I will attempt to calculate the square root of -16."}
    EXECUTE: {"step": "EXECUTE", "content": "Calculating sqrt", "tool_call": {"name": "calculate", "args": {"expression": "sqrt(-16)"}}}
    OBSERVE: {"step": "OBSERVE", "content": "Error: Math Domain Error (Cannot take square root of negative number)."}
    OUTPUT: {"step": "OUTPUT", "content": "I cannot calculate the square root of -16 because it results in an imaginary number, which is not supported by the current calculation tool."}
"""

SYSTEM_PROMPT = AGENT_PROMPT

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
                response_mime_type="application/json"
            )
        )

        text = response.text.strip()

        if not text:
            print("Model returned empty response")
            break

        # if not text.endswith("}"):
        #     text += "}"

        try:
            output = json.loads(text)
            step_type = output.get("step")

            if step_type == "EXECUTE":
                tool_call = output.get("tool_call")
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]

                # Logic to call your get_weather function
                if tool_name == "get_weather":
                    observation = get_weather(tool_args["city"])
                else:
                    observation = f"Error: Tool {tool_name} not found."

                # Manually create the OBSERVE step to give back to the model
                observe_step = {
                    "step": "OBSERVE",
                    "content": observation
                }
                print(f"[OBSERVE]: {observation}")
                
                chat_history.append({
                    "role": "user", # We send observation as 'user' or 'system' so model 'sees' it
                    "parts": [{"text": json.dumps(observe_step)}]
                })
                continue

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
