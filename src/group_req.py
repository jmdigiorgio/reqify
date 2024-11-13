import json
import os
from pathlib import Path

def extract_text_from_json(input_file, output_file):
    try:
        # Create data directory if it doesn't exist
        # Get the directory name from the output file path
        output_dir = os.path.dirname(output_file)
        if output_dir:
            # Create the output directory (and any parent directories) if it does not exist
            Path(output_dir).mkdir(parents=True, exist_ok=True)
            
        # Read and parse JSON file
        # Open the input JSON file for reading
        with open(input_file, 'r', encoding='utf-8') as f:
            # Load the JSON content into a Python object (usually a list or dictionary)
            data = json.load(f)
            
        # Extract text from each entry and join with newlines
        texts = []
        for entry in data:
            # Check if 'text' key exists in the current entry
            if 'text' in entry:
                # Strip any extra whitespace and add the text to the list
                texts.append(entry['text'].strip())
        
        # Combine all extracted text entries into a single string, separated by newlines
        combined_text = '\n'.join(texts)
        
        # Write combined text to output file
        # Open the output file for writing and save the combined text
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(combined_text)
            
        # Print success message
        print(f"Successfully extracted text and saved to {output_file}")
        return True
        
    # Handle case where the input file is not found
    except FileNotFoundError:
        print(f"Error: Could not find input file {input_file}")
        return False
    # Handle case where the input file is not a valid JSON
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {input_file}")
        return False
    # Handle any other unexpected errors
    except Exception as e:
        print(f"Error: An unexpected error occurred: {str(e)}")
        return False

def main():
    # Define the input and output file paths
    input_file = "data/out_clean_req/requirements.json"
    output_file = "data/out_group_req/requirements_all.txt"
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if output_dir:
        # Create the output directory (and any parent directories) if it does not exist
        Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Call the function to extract text from the JSON file
    success = extract_text_from_json(input_file, output_file)
    if not success:
        # If extraction fails, print an error message and exit with status code 1
        print("Failed to process the file")
        exit(1)

# Run the main function if this script is executed directly
if __name__ == "__main__":
    main()
