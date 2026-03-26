import os

from dotenv import load_dotenv

from functions.get_files_info import get_files_info

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# if len(sys.argv) < 2:
#     print("I need a prompt !!!")
#     sys.exit(1)
# prompt = sys.argv[1]

# messages = [
#     types.Content(role="user", parts=[types.Part(text=prompt)])
#     ]

# client = genai.Client(api_key=api_key)
# response = client.models.generate_content(
#     model="gemini-2.5-flash",
#     contents=messages,
# )

# print(response.text)
# if response.usage_metadata:
#     print(f"Prompt Tokens usage : {response.usage_metadata.prompt_token_count}")
#     print(f"Response tokens usage : {response.usage_metadata.candidates_token_count}")

files_info = get_files_info("calculator")
print(files_info)