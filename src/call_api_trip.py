import requests
import json
from dotenv import load_dotenv
import os


def main():
    # Load the API key
    load_dotenv(dotenv_path="api-key.env")
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API key is missing. Please check api-key.env")

    # Load the axiom prompt which stays the same for each API call
    with open("data/prompts/triples_prompt.txt", "r", encoding="utf-8") as file:
        axiom_prompt = file.read().strip()

    # Load the individual prompts from text files in the specified directory
    input_directory = "data/out_chunk_req/"
    doc_chunks = []

    # Iterate through all text files in the directory
    for filename in os.listdir(input_directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(input_directory, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                chunk_content = file.read().strip()
                doc_chunks.append({"filename": filename, "content": chunk_content})

    # Set the URL and headers for the API
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # Make a list to store API responses
    responses = []

    # Call the API for each chunk (file) in the directory
    for chunk in doc_chunks:
        # Structure the API call and designate the model used
        data = {
            "model": "gpt-4o",
            "messages": [
                {"role": "system", "content": axiom_prompt},
                {"role": "user", "content": chunk["content"]}
            ]
        }

        # Make the API call
        response = requests.post(url, headers=headers, json=data)

        # Check if the response was successful
        if response.status_code == 200:
            response_data = response.json()
            # Add the response to the list of responses
            responses.append({"filename": chunk["filename"], "response": response_data})
        else:
            print(f"Error with File '{chunk['filename']}': {response.status_code}, {response.text}")

        # User feedback for each chunk sent to the API
        print(f"File '{chunk['filename']}' sent to API")

    # Ensure the output directory exists
    output_directory = "data/out_call_api_trip/"
    os.makedirs(output_directory, exist_ok=True)

    # Save all API responses to a JSON file for clean up
    output_file_path = os.path.join(output_directory, "api_response.json")
    with open(output_file_path, "w", encoding="utf-8") as output_file:
        json.dump(responses, output_file, indent=4, ensure_ascii=False)

    print(f"API responses saved to '{output_file_path}'")


# Ensure main() only runs when this script is executed directly
if __name__ == "__main__":
    main()
