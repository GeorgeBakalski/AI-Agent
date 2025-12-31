import os, argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

def generate_content(client, messages, verbose):

    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents= messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
            )
    )

    metadata = response.usage_metadata
    if metadata  is None:
        raise RuntimeError("Response token count not found. Failed API request.")
    prompt_tokens = metadata.prompt_token_count
    response_tokens = metadata.candidates_token_count
    
    if verbose:
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")

    if not response.function_calls:
        print(f"Response: \n{response.text}")
        return 
    
    function_responses = []
    for function_call in  response.function_calls:
        function_call_result = call_function(function_call, verbose)

        if not function_call_result.parts:
            raise Exception("Function call returned no parts")

        if not function_call_result.parts[0].function_response:
            raise Exception("Missing FunctionResponse on part")
        
        if not function_call_result.parts[0].function_response.response:
            raise Exception("Empty function response payload")
        
        function_responses.append(function_call_result.parts[0])

        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")

def main():
    
    if api_key is None:
        raise RuntimeError("API key not found")
    
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    client = genai.Client(api_key=api_key)
    
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")

    generate_content(client, messages, args.verbose)

if __name__ == "__main__":
    main()
