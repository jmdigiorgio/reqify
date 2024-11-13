import json
import csv
import os

def main():
    input_path = 'data/out_call_api_trip/api_response.json'
    # Load the JSON file
    if not os.path.exists(input_path):
        print(f"Error: Input file not found at {input_path}")
        return
    
    with open(input_path, 'r') as file:
        data = json.load(file)

    # Extract triples from "content"
    triples = []
    for item in data:
        response_content = item.get("response", {}).get("choices", [])[0].get("message", {}).get("content", "")
        if response_content:
            # Split the content by periods and commas
            triples_content = response_content.split(".")
            for triple in triples_content:
                parts = [x.strip() for x in triple.split(",") if x.strip()]
                if len(parts) == 3:
                    triples.append(parts)

    # Ensure the output directory exists
    output_dir = 'data/out_clean_trip'
    os.makedirs(output_dir, exist_ok=True)

    # Write the triples to a CSV file
    with open(f'{output_dir}/triples.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Subject', 'Predicate', 'Object'])
        csvwriter.writerows(triples)

    print("CSV file created successfully.")

if __name__ == "__main__":
    main()
