import json
import os
import sys
from typing import cast

import openai
from dotenv import load_dotenv
from openai.types.chat import ChatCompletionMessageParam

from functions.call_functions import available_tools, function_map

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
MAX_ITERATIONS = 20

if len(sys.argv) < 2:
    print("I need a prompt !!!")
    sys.exit(1)
prompt = sys.argv[1]

system_prompt = """" You are a helpful coding AI agent.
    When the user asks a question or request, make a functional call plan. You can perform the following functions:
    - List files and directories
    - Read the contents of a file
    - Write content to a file
    - Run a python file with optional arguments.

    When the user asks a question about the project's code they are referring to the working directory. 
    So typically start by looking at the files in the project, then figure out how to run the project and project's tests.
    Validte that the project's tests pass to ensure the project behavior is correct.
    All paths you provide should be relative to the working folder. You do not need to specify the working folder as it will be automatically injected for security reasons.
    """


messages: list[ChatCompletionMessageParam] = [
    {"role": "user", "content": prompt},
    {"role": "system", "content": system_prompt},
]

client = openai.Client(api_key=api_key)

for i in range(MAX_ITERATIONS):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=cast(list[ChatCompletionMessageParam], messages),
        temperature=0.1,
        tool_choice="auto",
        tools=available_tools,
    )
    assistant_message = response.choices[0].message
    messages.append(cast(ChatCompletionMessageParam, assistant_message))

    tool_calls = assistant_message.tool_calls
    if tool_calls:
        for tool_call in tool_calls:
            if tool_call.type == "function":
                func_name = tool_call.function.name
                func_args_str = tool_call.function.arguments
                func_args = json.loads(func_args_str)
                print(f"Calling function: {func_name}({func_args})")
                result = function_map[func_name](working_dir=".", **func_args)
                # print(f"result of function call : {result}")
                # print(f"tool-call.id: {tool_call.id}")
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(result),
                    }
                )
            # args = json.loads(tool_call.function.arguments)

    else:
        print(response.choices[0].message.content)
        exit()
