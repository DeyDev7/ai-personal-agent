import argparse
import os


from dotenv import load_dotenv
from openai import OpenAI


# Defaults from OpenAI
BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "openrouter/free"


def get_api_key():
    load_dotenv()
    return os.environ.get("OPENROUTER_API_KEY")


def generate_response_from_model(client, user_prompt):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": user_prompt,
            }
        ],
    )

    if response.usage is None:
        raise RuntimeError("Failed API request | None value for response.usage")

    return (
        response.choices[0].message.content,
        response.usage.prompt_tokens,
        response.usage.completion_tokens,
    )


def create_client(api_key):
    if api_key is None:
        raise RuntimeError("API KEY was not found | api_key value: None")

    return OpenAI(base_url=BASE_URL, api_key=api_key)


def main():

    parser = argparse.ArgumentParser(
        description="Chat Bot",
    ) # handles user prompt on terminal
    parser.add_argument("user_prompt", type=str, help="User Prompt")
    args = parser.parse_args()

    # Path to assure everything is going fine. If anything happens, this will catch it up - it should, at least
    api_key = get_api_key()
    client = create_client(api_key)
    answer, prompt_tokens, response_tokens = generate_response_from_model(client, user_prompt=args.user_prompt)

    print(answer)
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {response_tokens}")


if __name__ == "__main__":
    main()
