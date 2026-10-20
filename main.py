import argparse
import json
import os


# - Must import llm_guard to avoid jailbraking | it's a must. AGENT could be jailbroken with roleplaying and encoded msg
# from llm_guard.input_scanners import PromptInjection, TokenLimit 
# from llm_guard.output_scanners import Sensitive, Toxicity
from dotenv import load_dotenv
from openai import OpenAI


from prompts import system_prompt
from call_function import available_schemas


# Defaults from OpenAI
BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "openrouter/free"


def get_api_key():
    load_dotenv()
    return os.environ.get("OPENROUTER_API_KEY")


def generate_response_from_model(client, user_prompt):
    messages: list = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=available_schemas,
        temperature=0,
    )

    assistant_message = response.choices[0].message
    for tool_call in assistant_message.tool_calls or []:
        function_args = json.loads(tool_call.function.arguments or "{}")
        print(f"Calling function: {tool_call.function.name}({function_args})")

    if response.usage is None:
        raise RuntimeError("Failed API request | None value for response.usage")

    return (
        assistant_message.content,
        response.usage.prompt_tokens,
        response.usage.completion_tokens,
    )


def create_client(api_key):
    if api_key is None:
        raise RuntimeError("API KEY was not found | api_key_value: None")

    return OpenAI(base_url=BASE_URL, api_key=api_key)


def main():

    parser = argparse.ArgumentParser(
        description="Chat Bot",
    ) # handles user prompt on terminal
    parser.add_argument("user_prompt", type=str, help="User Prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    # Path to assure everything is going fine. If anything happens, this will catch it up - it should, at least
    api_key = get_api_key()
    client = create_client(api_key)
    answer, prompt_tokens, response_tokens = generate_response_from_model(
        client,
        user_prompt=args.user_prompt
        )

    print(answer)
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {response_tokens}")


if __name__ == "__main__":
    main()
