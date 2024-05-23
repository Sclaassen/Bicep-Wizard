from dotenv import load_dotenv
import os
import re
from openai import OpenAI
from findService import find_service_directories, get_main_bicep_directories, user_select_service, user_select_directory

working_directory = os.path.dirname(os.path.abspath(__file__))
# Load environment variables from .env file
load_dotenv('.env')

print("""\nWelcome to Bicep Wizard!!!\n
╔╗ ╦╔═╗╔═╗╔═╗  ╦ ╦╦╔═╗╔═╗╦═╗╔╦╗
╠╩╗║║  ║╣ ╠═╝  ║║║║╔═╝╠═╣╠╦╝ ║║
╚═╝╩╚═╝╚═╝╩    ╚╩╝╩╚═╝╩ ╩╩╚══╩╝""")

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def prompt_user(prompt):
    return input(prompt)

def get_chatgpt_response(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that creates Bicep templates to be deployed to Azure."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1200,
            temperature=0.2
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return str(e)

def verify_private_endpoints(response):
    private_endpoint_keywords = ["privateEndpoint", "privateDnsZone", "privateDnsZoneLink", "privateEndpointDnsZoneGroup"]
    for keyword in private_endpoint_keywords:
        if keyword not in response:
            print(f"Warning: {keyword} not found in the generated template.")
    return response

def fix_bicep_template(content):
    content = content.replace('```bicep', '').replace('```', '').strip()
    if 'param location string' not in content:
        content = 'param location string\n' + content
    content = re.sub(r'location\s*=\s*[\w.]+\.location', 'location: location', content)
    content = re.sub(
        r"'Microsoft\.Network/virtualNetworks@[\d-]+/virtualNetworkLinks@[\d-]+'", 
        "'Microsoft.Network/privateDnsZones/virtualNetworkLinks@2020-06-01'", 
        content
    )
    return content

def main():
    local_directory = 'D:\\Bicep-Templates\\bicep_env\\src\\avm\\res'  # Define the base directory to search
    
    while True:
        service_name = prompt_user("Enter the service name to search for: ")  # User input for the service name

        matching_directories = find_service_directories(local_directory, service_name)
        if not matching_directories:
            print("No matching services found.")
        else:
            selected_directory = user_select_service(matching_directories)
            main_bicep_directories = get_main_bicep_directories(selected_directory)
            if not main_bicep_directories:
                print("No services containing 'main.bicep' found.")
            else:
                selected_main_bicep_directory = user_select_directory(main_bicep_directories)
                print(f"Please Wait...Generating Bicep Template for {service_name}...")
                # Fetch content for the first main.bicep file in the selected directory
                bicep_file_path = os.path.join(selected_main_bicep_directory, 'main.bicep')
                with open(bicep_file_path, 'r') as file:
                    avm_module_content = file.read()

                prompt_text = (
                    f"Before  you do anything browse the internet and check if the service can integrate with the virtual network via a private endpoint. \n"
                    f"Create a container app Bicep template based on the following requirements:\n"
                    f"Comprehensive network security, encryption settings, and secure access configurations.\n"
                    f"Extensive, well-documented parameters with descriptions and allowed values.\n"
                    f"Use the latest Azure Bicep features\n"
                    f"Use the latest Azure Bicep best practices\n"
                    f"Use the latest Azure Bicep patterns\n"
                    f"Use the latest Azure Bicep naming conventions\n"
                    f"Add comments to response\n"
                    f"Follow Azure Well-Architected Framework\n"
                    f"Use the following Bicep module as a Benchmark to create a simplistic {service_name}\n"
                    f"Do not add any @description or @metadata\n"
                    f"do not over-parameterize the code"
                    # f"Create a Bicep template based on the following requirements:\n"
                    # f"- Comprehensive network security, encryption settings, and secure access configurations.\n"
                    # f"- Before  you do anything browse the internet and check if the service can integrate with the virtual network via a private endpoint. If it can, include private endpoints in the Bicep template\n"
                    # #f"- Include private DNS zones, private DNS zone links and the private endpoint DNS zone group if the service can utilize it\n"
                    # f"- Service should be connected to the virtual network\n"
                    # f"- Service should be connected to the subnet\n"
                    # f"- service should not be exposed to the internet\n"
                    # f"- Include parameters for customization\n"
                    # f"- Use the latest Azure Bicep features\n"
                    # f"- Use the latest Azure Bicep best practices\n"
                    # f"- Use the latest Azure Bicep patterns\n"
                    # f"- Use the latest Azure Bicep naming conventions\n"
                    # f"- NO comments in response\n"
                    # f"- Follow Azure Well-Architected Framework\n"
                    # f"- Use the following Bicep module as a Benchmark to create a simplistic {service_name}\n"
                    # f"- Do not add any @description or @metadata\n"
                    # f"- do not over parameterize the code\n"
                    # f"- Provide only the Bicep code without any additional explanation or placeholders."
                    # f"provide the filename for the Bicep template\n"
                )
                response = get_chatgpt_response(prompt_text)
                response = verify_private_endpoints(response)
                fixed_response = fix_bicep_template(response)

                # Ask the user for the filename and check that it is not empty
                filename = prompt_user("Provide the filename for the Bicep template: ").strip()
                if not filename:
                    print("Filename cannot be empty.")
                    continue
                if not filename.endswith('.bicep'):
                    filename += '.bicep'

                # Save the file to working_directory/outputBicepTemplates
                output_directory = os.path.join(working_directory, 'outputBicepTemplates')
                if not os.path.exists(output_directory):
                    os.makedirs(output_directory)

                output_path = os.path.join(output_directory, filename)
                with open(output_path, 'w') as file:
                    file.write(fixed_response)

                print(f"Fixed Bicep template saved as {filename}")

        another_service = prompt_user("Do you want to search for another service? (yes/no): ").strip().lower()
        if another_service != 'yes':
            break

if __name__ == "__main__":
    main()
