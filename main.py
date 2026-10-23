import argparse
import os
import sys


# Must import llm_guard to avoid jailbraking
# it's a must. AGENT could be jailbroken with roleplaying and encoded msg
# from llm_guard.input_scanners import PromptInjection, TokenLimit 
# from llm_guard.output_scanners import Sensitive, Toxicity

from dotenv import load_dotenv
from openai import OpenAI


from prompts import system_prompt
from call_function import available_schemas, call_function


# Defaults from OpenAI
BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "openrouter/free"


def get_api_key():
    load_dotenv()
    return os.environ.get("OPENROUTER_API_KEY")


def generate_response_from_model(client, user_prompt, verbose: bool = False):
    messages: list = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    total_prompt_tokens = 0
    total_completion_tokens = 0

    for _ in range(20):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=available_schemas,
            temperature=0,
        )

        message = response.choices[0].message
        messages.append(message)

        if response.usage is None:
            raise RuntimeError("Failed API request | None value for response.usage")

        total_prompt_tokens += response.usage.prompt_tokens
        total_completion_tokens += response.usage.completion_tokens

        for tool_call in message.tool_calls or []:
            result_message = call_function(tool_call, verbose=verbose)
            if not result_message.get("content"):
                raise RuntimeError("Function call returned an empty tool response")
            messages.append(result_message)
            if verbose:
                print(f"-> {result_message['content']}")

        if not message.tool_calls:
            return (
                message.content,
                total_prompt_tokens,
                total_completion_tokens,
            )

    raise RuntimeError("Model did not complete the task within 20 turns")


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

    try:
        api_key = get_api_key()
        client = create_client(api_key)
        answer, prompt_tokens, response_tokens = generate_response_from_model(
            client,
            user_prompt=args.user_prompt,
            verbose=args.verbose,
        )
    except RuntimeError as err:
        print(f"Error: {err}", file=sys.stderr)
        return 1

    print(answer)
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {response_tokens}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
