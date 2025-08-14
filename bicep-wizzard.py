import os
from pathlib import Path
from typing import Optional

import google.generativeai as genai


def generate_bicep_template(
    filename: str = "storage_account_template.bicep",
    prompt_override: Optional[str] = None,
) -> str:
    """Generate a storage account Bicep template and save it to ``filename``.

    Parameters
    ----------
    filename:
        Name of the file to write the generated template to.
    prompt_override:
        Optional prompt string to send to the model instead of the default
        storage account request.

    Returns
    -------
    str
        The path to the file containing the generated template.
    """

    api_key = os.getenv("API_KEY")
    if not api_key:
        raise EnvironmentError("API_KEY environment variable not set")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-pro")

    prompt_parts = [
        "Write a Bicep template to create a Storage account",
        "It needs to strictly follow the Azure well-architected framework.",
        "Requirements: Private Endpoint, Private DNS, VNet",
    ]
    prompt = prompt_override or " ".join(prompt_parts)

    try:
        response = model.generate_content(prompt)
    except Exception as exc:  # pragma: no cover - network failure etc.
        raise RuntimeError("Failed to generate Bicep template") from exc

    output_path = Path(filename)
    output_path.write_text(response.text, encoding="utf-8")
    return str(output_path)


if __name__ == "__main__":
    saved_file = generate_bicep_template()
    print(f"Bicep template saved as {saved_file}")
