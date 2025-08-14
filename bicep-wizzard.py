import os
import google.generativeai as genai


def generate_bicep_template() -> None:
    """Generate a storage account Bicep template and save it to disk."""

    api_key = os.environ.get("API_KEY")
    if not api_key:
        raise ValueError("API_KEY environment variable not set")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-pro")

    prompt = (
        "Write a Bicep template to create a Storage account, it needs to strictly follow "
        "the Azure well-architected framework. Requirements: Private Endpoint, Private DNS, VNet"
    )

    response = model.generate_content(prompt)
    print(response.text)

    filename = "storage_account_template.bicep"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(response.text)

    print(f"Bicep template saved as {filename}")


if __name__ == "__main__":
    generate_bicep_template()
