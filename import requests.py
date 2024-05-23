try:
    import requests
    from bs4 import BeautifulSoup
    import os
except ImportError:
    import os
    os.system('pip install requests beautifulsoup4')
    import requests
    from bs4 import BeautifulSoup

# Base URL of the Azure templates page
base_url = 'https://learn.microsoft.com/en-us/azure/templates/'

# Function to scrape the Bicep templates
def scrape_bicep_templates(base_url):
    response = requests.get(base_url)
    if response.status_code != 200:
        print(f"Failed to retrieve the page: {response.status_code}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    reference_menu = soup.find('nav', {'class': 'nav--reference'})  # Adjust this selector as needed
    
    if not reference_menu:
        print("Reference menu not found.")
        return

    template_links = reference_menu.find_all('a')

    for link in template_links:
        resource_name = link.text.strip()
        resource_url = link['href']
        full_url = f"https://learn.microsoft.com{resource_url}"
        
        print(f"Scraping resource: {resource_name} from {full_url}")
        
        scrape_and_create_bicep_file(resource_name, full_url)

def scrape_and_create_bicep_file(resource_name, resource_url):
    response = requests.get(resource_url)
    if response.status_code != 200:
        print(f"Failed to retrieve the resource page: {response.status_code}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    code_blocks = soup.find_all('pre', {'class': 'lang-bicep'})

    if not code_blocks:
        print(f"No Bicep code found for {resource_name}")
        return

    # Assume the first code block is the relevant Bicep template
    bicep_code = code_blocks[0].text

    # Clean resource name for file naming
    clean_resource_name = resource_name.replace(' ', '_').replace('/', '_')
    file_name = f"{clean_resource_name}.bicep"

    with open(file_name, 'w') as file:
        file.write(bicep_code)

    print(f"Bicep template for {resource_name} saved as {file_name}")

# Create a directory to store the Bicep files
output_directory = 'bicep_templates'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Change the current directory to the output directory
os.chdir(output_directory)

# Start scraping
scrape_bicep_templates(base_url)

print("Scraping completed.")
