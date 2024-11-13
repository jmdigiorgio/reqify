import os
import re
import tiktoken

# Function to split text into chunks of 3000 tokens without cutting mid-sentence
def split_text_into_chunks(text, max_tokens, tokenizer):
    # Split text into sentences using punctuation marks (., ?, !) as delimiters
    sentences = re.split(r'(\.|\?|!)', text)
    chunks = []  # List to store the chunks of text
    current_chunk = ""  # Variable to store the current chunk being built
    current_tokens = 0  # Counter for the number of tokens in the current chunk

    # Iterate over the sentences in pairs (sentence and its punctuation)
    for i in range(0, len(sentences) - 1, 2):
        sentence = sentences[i] + sentences[i + 1]  # Reconstruct sentence with punctuation
        sentence_tokens = len(tokenizer.encode(sentence))  # Get the number of tokens in the sentence

        # Check if adding the current sentence would exceed the maximum token limit
        if current_tokens + sentence_tokens > max_tokens:
            # If it exceeds, save the current chunk and start a new one
            chunks.append(current_chunk.strip())
            current_chunk = sentence
            current_tokens = sentence_tokens
        else:
            # Otherwise, add the sentence to the current chunk
            current_chunk += sentence
            current_tokens += sentence_tokens

    # Add the last chunk if there is any remaining text
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

def main():
    # Load the text from requirements.txt
    input_file = 'data/out_group_req/requirements_all.txt'
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            text = file.read()  # Read the entire content of the input file
    except FileNotFoundError:
        print(f"Error: The file {input_file} does not exist.")
        return

    # Initialize tokenizer (using tiktoken, compatible with OpenAI models)
    tokenizer = tiktoken.get_encoding("cl100k_base")

    # Split text into chunks of 3000 tokens or less
    max_tokens = 2000
    chunks = split_text_into_chunks(text, max_tokens, tokenizer)

    # Save each chunk to a separate file in the output folder
    output_folder = 'data/out_chunk_req'
    os.makedirs(output_folder, exist_ok=True)  # Create the output directory if it doesn't exist

    # Iterate over each chunk and save it to a separate file
    for idx, chunk in enumerate(chunks, start=1):
        output_file = f'{output_folder}/requirements_{idx}.txt'
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(chunk)  # Write the chunk to the output file
        print(f"Saved chunk {idx} to {output_file}")

if __name__ == "__main__":
    main()
