# This script is intended to be run after call_api.py and cleans the API response data

import json
import re
import os
from typing import List, Optional, Dict, Union, Any

class JSONExtractor:
    """A class to handle extraction of JSON content from various formats."""
    
    @staticmethod
    def extract_from_code_blocks(content: str) -> List[str]:
        """Extract JSON content from markdown code blocks."""
        # This method searches for JSON content within markdown code blocks using a regular expression.
        code_block_pattern = re.compile(r'```(?:json)?\s*(.*?)```', re.DOTALL | re.IGNORECASE)
        return [match.strip() for match in code_block_pattern.findall(content)]
    
    @staticmethod
    def extract_raw_json(content: str) -> Optional[str]:
        """Extract JSON content that's not in code blocks."""
        # This method searches for JSON content that is not wrapped in code blocks.
        json_pattern = re.compile(r'(\{.*?\}|\[.*?\])', re.DOTALL)
        match = json_pattern.search(content)
        return match.group(1).strip() if match else None
    
    @staticmethod
    def clean_json_string(json_str: str) -> str:
        """Clean JSON string by removing trailing commas and extra whitespace."""
        # Remove trailing commas before closing braces/brackets
        json_str = re.sub(r',\s*(\}|\])', r'\1', json_str)
        # Remove any leading/trailing whitespace
        return json_str.strip()

    @staticmethod
    def parse_json(json_str: str) -> Optional[Union[Dict, List]]:
        """Safely parse a JSON string."""
        # Attempt to parse the JSON string and return None if it fails.
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            return None

class APIResponseCleaner:
    """A class to clean and process API responses."""
    
    def __init__(self, input_file: str, output_file: str):
        # Initialize the cleaner with input and output file paths.
        self.input_file = input_file
        self.output_file = output_file
        self.json_extractor = JSONExtractor()
        self.collected_objects: List[Dict] = []
        
    def load_input_file(self) -> List[Dict]:
        """Load and parse the input file."""
        # This method attempts to load the input file as JSON.
        try:
            with open(self.input_file, 'r', encoding='utf-8') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    # If the file is in JSON Lines format, read each line separately.
                    f.seek(0)
                    return [json.loads(line) for line in f if line.strip()]
        except Exception as e:
            print(f"Error loading input file: {e}")
            return []

    def process_content(self, content: str, entry_idx: int) -> None:
        """Process content to extract JSON objects."""
        # Attempt to extract JSON content from code blocks first.
        json_blocks = self.json_extractor.extract_from_code_blocks(content)
        
        if not json_blocks:
            # If no code blocks are found, attempt to extract raw JSON.
            raw_json = self.json_extractor.extract_raw_json(content)
            if raw_json:
                json_blocks = [raw_json]
            else:
                print(f"[Entry {entry_idx}] JSON content not found. Skipping this entry.")
                return

        # Process each JSON block that was extracted.
        for json_str in json_blocks:
            cleaned_json = self.json_extractor.clean_json_string(json_str)
            
            try:
                parsed_json = self.json_extractor.parse_json(cleaned_json)
                if parsed_json is None:
                    continue
                
                # Handle both single JSON objects and arrays of objects.
                if isinstance(parsed_json, dict):
                    self.collected_objects.append(parsed_json)
                elif isinstance(parsed_json, list):
                    self.collected_objects.extend(parsed_json)
                    
            except json.JSONDecodeError as e:
                print(f"[Entry {entry_idx}] Error decoding JSON content: {e}")
                print(f"[Entry {entry_idx}] JSON content that caused the error:\n{cleaned_json}\n")

    def process_responses(self) -> None:
        """Process all API responses."""
        # Load the list of responses from the input file.
        data_list = self.load_input_file()
        
        # Iterate through each entry in the data list and process it.
        for idx, data_dict in enumerate(data_list, start=1):
            try:
                # Extract the content from the response dictionary.
                content = data_dict['response']['choices'][0]['message']['content']
                self.process_content(content, idx)
            except (KeyError, IndexError, TypeError) as e:
                # Handle cases where expected keys are missing.
                print(f"[Entry {idx}] Skipping due to missing keys: {e}")
                continue

    def save_output(self) -> None:
        """Save processed JSON objects to output file."""
        # Ensure the output directory exists.
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        
        # Write the collected JSON objects to the output file.
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(self.collected_objects, f, indent=4, ensure_ascii=False)
        
        print(f"Collected {len(self.collected_objects)} JSON objects and wrote them to '{self.output_file}'.")

def main():
    # Define the input and output file paths.
    input_file = 'data/out_call_api_req/api_response.json'
    output_file = 'data/out_clean_req/requirements.json'
    
    # Check if the input file exists, otherwise raise an error.
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"The file '{input_file}' does not exist.")
    
    # Create an instance of APIResponseCleaner and run the processing steps.
    cleaner = APIResponseCleaner(input_file, output_file)
    cleaner.process_responses()
    cleaner.save_output()

if __name__ == "__main__":
    main()
