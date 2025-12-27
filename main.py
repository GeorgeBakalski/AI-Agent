import os, argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

def main():
    
    if api_key is None:
        raise RuntimeError("API key not found")
    
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
    model='gemini-2.5-flash', contents= messages
    )
    metadata = response.usage_metadata
    if metadata  is None:
        raise RuntimeError("Response token count not found. Failed API request.")
    prompt_tokens = metadata.prompt_token_count
    response_tokens = metadata.candidates_token_count
    
    if args.verbose == True:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")
    print(f"Response: \n{response.text}")

if __name__ == "__main__":
    main()
