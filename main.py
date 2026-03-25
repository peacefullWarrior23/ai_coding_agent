import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if len(sys.argv) < 2:
    print("I need a prompt !!!")
    sys.exit(1)
prompt = sys.argv[1]

messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)])
    ]

client = genai.Client(api_key=api_key)
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=messages,
)

print(response.text)
if response.usage_metadata:
    print(f"Prompt Tokens usage : {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens usage : {response.usage_metadata.candidates_token_count}")
