"""
import os
api_key = os.getenv('GEMINI_API_KEY')  # Ensure your API key is set in the environment variables
print(api_key)
"""
import google.generativeai as genai
import os

api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("GEMINI_API_KEY environment variable not set.")
else:
    genai.configure(api_key=api_key)
    models = genai.list_models()
    for model in models:
        print(f"Model: {model.name}")
        print(f"  Description: {model.description}")
        print(f"  Generation Methods: {model.supported_generation_methods}")
        print("-" * 20)