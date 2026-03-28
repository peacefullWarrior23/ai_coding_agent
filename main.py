import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.call_functions import available_functions, call_function

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
MAX_ITERATIONS = 20

if len(sys.argv) < 2:
    print("I need a prompt !!!")
    sys.exit(1)
prompt = sys.argv[1]

messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]
system_prompt = (
    """" You are a helpful coding AI agent.
    When the user asks a question or request, make a functional call plan. You can perform the following functions:
    - List files and directories
    - Read the contents of a file
    - Write content to a file
    - Run a python file with optional arguments
    All paths you provide should be relative to the working folder. You do not need to specify the working folder as it will be automatically injected for security reasons.
    """
)

client = genai.Client(api_key=api_key)

for i in range(MAX_ITERATIONS):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions]
        )
    )
    if response.candidates:
        for candidate in response.candidates:
            if candidate and candidate.content:
                messages.append(candidate.content)

    if response.function_calls:
        for function_call in response.function_calls:
            result = call_function(function_call, verbose=True)
            messages.append(result)
    else:
        print(response.text)
        exit()
    

# if response.usage_metadata:
#     print(f"Prompt Tokens usage : {response.usage_metadata.prompt_token_count}")
#     print(f"Response tokens usage : {response.usage_metadata.candidates_token_count}")
