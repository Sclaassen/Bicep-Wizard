from dotenv import load_dotenv
import os
import re
from openai import OpenAI

# Load environment variables from .env file
load_dotenv('.env')

def sanitizeBicepTemplate(content):
    content = content.replace('```bicep', '').replace('```', '').strip()
    if 'param location string' not in content:
        content = 'param location string\n' + content
    content = re.sub(r'location\s*=\s*[\w.]+\.location', 'location: location', content)
    return content
print("""\nWelcome to Bicep Wizard!!!\n
╔╗ ╦╔═╗╔═╗╔═╗  ╦ ╦╦╔═╗╔═╗╦═╗╔╦╗
╠╩╗║║  ║╣ ╠═╝  ║║║║╔═╝╠═╣╠╦╝ ║║
╚═╝╩╚═╝╚═╝╩    ╚╩╝╩╚═╝╩ ╩╩╚══╩╝""")
# Initialize OpenAI client
def prompt_user(prompt):
    return input(prompt)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

service_name = prompt_user("\nEnter the Azure service to search for: \n")

def get_chatgpt_response(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.8
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return str(e)

prompt = (
                    f"Create a Bicep template based on the following requirements:\n"
                    f"- Include private endpoints only for services that support them\n"
                    f"- For services that do not support private endpoints, link them to the virtual network in the best way possible\n"
                    f"- If the service supports private endpoints include private DNS zones, private DNS zone links and the private endpoint DNS zone group\n"
                    f"- Include parameters for customization\n"
                    f"- Use the latest Azure Bicep features\n"
                    f"- Use the latest Azure Bicep best practices\n"
                    f"- Use the latest Azure Bicep patterns\n"
                    f"- Use the latest Azure Bicep naming conventions\n"
                    f"- NO comments in response\n"
                    f"- Follow Azure Well-Architected Framework\n"
                    #f"- Specific template details: {service_name}\n"
                    f"- Use to the following bicep module as a Benchmark to create a simplistic  {service_name}\n"
                    f"- Do not add any @description or @metadata\n"
                    f"- do not over parameterize the code\n"
                    f"- Provide only the Bicep code without any additional explanation or placeholders."
                    # f"provide the filename for the Bicep template\n"
                )

aiResponse = get_chatgpt_response(prompt)
sanitizedResponse = sanitizeBicepTemplate(aiResponse)
# Ask the user for the filename
filename = prompt_user("Provide the filename for the Bicep template: ").strip()
if not filename.endswith('.bicep'):
    filename += '.bicep'

with open(filename, 'w') as file:
    file.write(sanitizedResponse)

print(f"Bicep template saved as {filename}")