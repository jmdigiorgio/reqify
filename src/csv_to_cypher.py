import pandas as pd
import os
import re

def escape_quotes(value):
    # Escape single quotes and other special characters for Cypher compatibility
    return re.sub(r"'", "\\'", value)

def sanitize_relationship(value):
    # Replace any non-alphanumeric characters with underscores for valid relationship names
    return re.sub(r"[^a-zA-Z0-9_]", "_", value)

def generate_cypher_script(file_path, output_dir):
    # Load the CSV file
    triples_df = pd.read_csv(file_path)

    # Initialize sets to keep track of unique subjects and objects
    unique_nodes = set()
    cypher_statements = []

    # Create unique node creation statements for subjects and objects
    for _, row in triples_df.iterrows():
        subject = escape_quotes(row['Subject'])
        obj = escape_quotes(row['Object'])
        predicate = sanitize_relationship(row['Predicate']).upper()
        
        # Add subject and object to unique nodes set
        unique_nodes.add(subject)
        unique_nodes.add(obj)
        
        # Create relationship statement
        relationship_statement = f"MATCH (a:Node {{name: '{subject}'}}), (b:Node {{name: '{obj}'}}) CREATE (a)-[:{predicate}]->(b);"
        cypher_statements.append(relationship_statement)

    # Create node creation statements
    node_statements = [f"MERGE (n:Node {{name: '{node}'}});" for node in unique_nodes]

    # Combine node and relationship statements
    full_cypher_script = "\n".join(node_statements + cypher_statements)

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Output the generated Cypher script
    output_path = os.path.join(output_dir, 'triples.cypher')
    with open(output_path, 'w') as file:
        file.write(full_cypher_script)

    print(f"Cypher script has been generated and saved as '{output_path}'")

def main():
    input_file_path = 'data/out_clean_trip/triples.csv'
    output_directory = 'data/out_csv_to_cypher'
    generate_cypher_script(input_file_path, output_directory)

if __name__ == "__main__":
    main()
