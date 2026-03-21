from google import genai
import os
from dotenv import load_dotenv
import json

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Chain of thought prompting involves letting the model to list out the way it is thinking and acting to get a solution to the user query

CHAIN_OF_THOUGHT_PROMPT = """
    You are an expert AI assistant that can easily resolve user queries using chain of thought.
    You work on START,PLAN and OUTPUT steps.
    You need to forst PLAN what needs to be done. PLAN can be in multiple steps. The final step is OUTPUT.
    Once enpught planning is done you can provide the OUTPUT.

    Rule:
    - Strictly provide the output in JSON format
    - Only run one step at a time
    - The sequence of steps is START where user provides query, the PLAN steps (multiple ) where you tell what you are thinking of, 
    and then finally OUTPUT step where you provide the final output

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

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
        # Below method of system prompting is not allowed in gemini 
        # {"role":"system","parts":[{"text":"SYSTEM_PROMPT"}]},
        {"role":"user","parts":[{"text":"C++ code to add two numbers"}]},
        # Right now we are manually adding chat history for each step, we can automate this as well.
        {
            "role": "model",
            "parts": [{"text": json.dumps({
                "step": "PLAN",
                "content": "The user wants a C++ code snippet to add two numbers. I will provide a simple program that takes two integers as input from the user, adds them, and then displays the result."
            })}]
        }
    ],
    config=genai.types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT
    )
)

# Final Response
# {"step": "PLAN", "content": "I need to include the iostream header for input/output operations, use the std namespace, define a main function, declare two integer variables for input, a third for the sum, prompt the user for input, read the inputs, perform the addition, and then print the result."}
# {"step": "OUTPUT", "content": "```cpp\n#include <iostream>\n\nint main() {\n    // Declare variables to store the two numbers and their sum\n    int num1, num2, sum;\n\n    // Prompt the user to enter the first number\n    std::cout << \"Enter the first number: \";\n    // Read the first number from the user\n    std::cin >> num1;\n\n    // Prompt the user to enter the second number\n    std::cout << \"Enter the second number: \";\n    // Read the second number from the user\n    std::cin >> num2;\n\n    // Calculate the sum of the two numbers\n    sum = num1 + num2;\n\n    // Display the result\n    std::cout << \"The sum of \" << num1 << \" and \" << num2 << \" is: \" << sum << std::endl;\n\n    return 0;\n}\n```"}

print(response.text)