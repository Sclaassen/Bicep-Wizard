import os
import subprocess
import google.generativeai as genai

def prompt_user(prompt):
    return input(prompt)

# Ensure the API key is set in the environment
api_key = os.environ.get("API_KEY")
if not api_key:
    raise ValueError("API_KEY environment variable not set")

# Configure the generative AI model
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro')

# Get the requirements from the user
requirements = prompt_user("Which Bicep template do you want to create? ")

# Generate the Bicep template content
response = model.generate_content(f"create a bicep template based on requirements, needs to include private endpoints, Private DNS with parameters. Needs to follow the Azure well-architected framework.do not add any comments {requirements}")

# Define the filename for the Bicep template
filename = 'storage_account_template.bicep'

# Write the generated content to a Bicep file
with open(filename, 'w') as file:
    file.write(response.text)

print(f"Generated Bicep template saved as {filename}")

# Validate the Bicep template using bicep CLI
bicep_config_path = '/mnt/data/bicepconfig.json'
validation_result = subprocess.run(['bicep', 'build', filename, '--no-restore'], capture_output=True, text=True)

# Check for validation errors
if validation_result.returncode != 0:
    print("Validation errors found:")
    print(validation_result.stderr)
else:
    print("No validation errors found.")

# Fix common errors in the Bicep template
with open(filename, 'r') as file:
    bicep_content = file.read()

# Fix unexpected new line characters after commas
bicep_content = bicep_content.replace(',\n', ',')

# Fix the location assignment issue
bicep_content = bicep_content.replace('location = storageAccount.location', 'location = resourceGroup().location')

# Save the fixed template
fixed_filename = 'fixed_storage_account_template.bicep'
with open(fixed_filename, 'w') as file:
    file.write(bicep_content)

print(f"Fixed Bicep template saved as {fixed_filename}")
