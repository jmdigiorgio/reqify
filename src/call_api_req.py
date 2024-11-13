import requests
import json
from dotenv import load_dotenv
import os
import glob

def main():
    # Load the API key
    load_dotenv(dotenv_path="api-key.env")
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API key is missing. Please check api-key.env")

    # Load the system prompt which stays the same for each API call
    with open("data/prompts/system_prompt.txt", "r", encoding="utf-8") as file:
        system_prompt = file.read().strip()

    # Find the input file in data/out_chunk_pdf
    input_files = glob.glob("data/out_chunk_pdf/*.json")
    if not input_files:
        raise FileNotFoundError("No input file found in data/out_chunk_pdf")
    input_file_path = input_files[0]

    # Load the individual prompts which differ for each API call
    with open(input_file_path, "r", encoding="utf-8") as file:
        doc_chunks = json.load(file)

    # Set the URL and headers for the API
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # Make a list to store API responses
    responses = []

    # Call the API for each chunk that the PDF has been divided into
    for chunk in doc_chunks:
        # Structure the API call and designate the model used
        data = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Chunk ID: {chunk['chunk_id']} {chunk['chunk']}"}
            ]
        }

        # Make the API call
        response = requests.post(url, headers=headers, json=data)

        # Check if the response was successful
        if response.status_code == 200:
            response_data = response.json()
            # Add the response to the list of responses
            responses.append({"chunk_id": chunk["chunk_id"], "response": response_data})
        else:
            print(f"Error with Chunk ID {chunk['chunk_id']}: {response.status_code}, {response.text}")

        # User feedback for each chunk sent to the API
        print(f"Chunk ID {chunk['chunk_id']} sent to API")

    # Ensure the output directory exists
    output_directory = "data/out_call_api_req"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Save all API responses to a JSON file for clean up
    output_file_path = os.path.join(output_directory, "api_response.json")
    with open(output_file_path, "w", encoding="utf-8") as output_file:
        json.dump(responses, output_file, indent=4, ensure_ascii=False)

    print(f"API responses saved to '{output_file_path}'")

# Ensure main() only runs when this script is executed directly
if __name__ == "__main__":
    main()
