import os


from dotenv import load_dotenv
from openai import OpenAI


# CONSTANTS
BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "openrouter/free"


def get_api_key():
    load_dotenv()

    return os.environ.get("OPENROUTER_API_KEY")


def generate_response_from_model(client):

    response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {
            "role": "user",
            "content": "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
        }
    ],
)
    return response.choices[0].message.content


def create_client(api_key):

    if api_key is None:
        raise RuntimeError("API KEY was not found | api_key value: None")

    return OpenAI(base_url=BASE_URL, api_key=api_key)


def main():
    api_key = get_api_key()
    client = create_client(api_key)
    answer = generate_response_from_model(client)

    print(answer)


if __name__ == "__main__":
    main()
