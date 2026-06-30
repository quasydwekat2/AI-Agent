import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt


def generate_content(client, messages):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0
        )
    )
    return response


def config_client():
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY not found.")

    return genai.Client(api_key=api_key)


def main():
    parser = argparse.ArgumentParser(description="Chatbot CLI")

    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    client = config_client()

    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=args.user_prompt)]
        )
    ]

    response = generate_content(client, messages)

    print(response.text)

    usage = response.usage_metadata

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {usage.prompt_token_count}")
        print(f"Response tokens: {usage.candidates_token_count}")


if __name__ == "__main__":
    main()