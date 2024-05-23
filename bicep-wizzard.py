import os
import google.generativeai as genai

# Ensure the API key is set in the environment
api_key = os.environ.get("API_KEY")

# Check if the API key is available
if not api_key:
    raise ValueError("API_KEY environment variable not set")

# Configure the generative AI model
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro')

# Generate the Bicep template content
response = model.generate_content("Write a Bicep template to create a Storage account, it needs to strictly follow the Azure well-architected framework. Requirements: Private Endpoint, Private DNS, VNet")

# Print the response for verification
print(response.text)

# Define the filename for the Bicep template
filename = 'storage_account_template.bicep'

# Write the generated content to a Bicep file
with open(filename, 'w') as file:
    file.write(response.text)

print(f"Bicep template saved as {filename}")
