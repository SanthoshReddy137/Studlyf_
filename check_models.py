import os
import google.generativeai as genai

# Securely load your active API Key
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

print("--- FETCHING AUTHORIZED MODELS ---")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)