import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import available_functions, call_function


def generate_content(client, messages):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions],
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

    parser.add_argument("user_prompt", type=str)
    parser.add_argument("--verbose", action="store_true")

    args = parser.parse_args()

    client = config_client()

    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=args.user_prompt)]
        )
    ]

    response = generate_content(client, messages)

    # 🔥 Function calling logic
    if response.function_calls:
        function_results = []

        for function_call in response.function_calls:
            result = call_function(function_call, verbose=args.verbose)
            function_results.append(result)

            if args.verbose:
                fr = result.parts[0].function_response.response
                print(f"-> {fr}")

    else:
        print(response.text)


if __name__ == "__main__":
    main()