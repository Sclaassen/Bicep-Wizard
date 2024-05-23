
try:
    import google.generativeai as genai
except ImportError:
    pass


genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel('gemini-pro')


response = model.generate_content("Write me bicep template to create a Storage account.")
print(response.text)