import os
import google.generativeai as genai

def test_api():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        api_key = input("Please enter your GEMINI_API_KEY: ").strip()
        if not api_key:
            print("No API Key provided. Exiting.")
            return

    print(f"Using API Key: {api_key[:5]}...{api_key[-5:] if len(api_key)>10 else ''}")
    
    genai.configure(api_key=api_key)

    print("\n--- Listing Available Models ---")
    try:
        found_flash = False
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"- {m.name}")
                if "flash" in m.name:
                    found_flash = True
        
        print("\n--- Testing Generation ---")
        model_name = 'gemini-1.5-flash' if found_flash else 'gemini-pro'
        print(f"Trying model: {model_name}")
        
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Hello! Are you working?")
        print(f"Response: {response.text}")
        
    except Exception as e:
        print(f"API Error: {e}")

if __name__ == "__main__":
    test_api()
