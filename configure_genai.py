import os
import google.generativeai as genai

api_key = os.environ["API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro')

response = model.generate_content("Write a bicep template to create a Storage account, it needs to strickly follow the Azure well-architected framework. Requirements: Private Endpoint, Private DNS, vnet")
print(response.text)
