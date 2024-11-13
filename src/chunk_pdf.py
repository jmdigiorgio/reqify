import PyPDF2
import nltk
import json
import re
import os

# Download necessary NLTK data
def download_nltk_resources():
    # Try to find the 'punkt' tokenizer, download it if it's not available
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')

# Extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    # Open the PDF file in binary read mode
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        # Iterate through each page in the PDF and extract text
        for page_num, page in enumerate(reader.pages, start=1):
            page_text = page.extract_text()
            if page_text:
                # Append the page number and the extracted text
                text += f'Page {page_num}:' + page_text + '\n'
    return text

# Clean the extracted text
def clean_text(text):
    # Replace all whitespace characters (including newlines and tabs) with a single space
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Split the text into chunks based on sentence count and word limit
def item_text_by_sentence(text, item_word_limit=500):
    # Split the text into individual sentences using NLTK's tokenizer
    sentences = nltk.tokenize.sent_tokenize(text)
    items = []
    current_item = []
    current_word_count = 0

    # Iterate over each sentence and group them into chunks based on the word limit
    for sentence in sentences:
        word_count = len(sentence.split())
        if current_word_count + word_count <= item_word_limit:
            # Add the sentence to the current chunk
            current_item.append(sentence)
            current_word_count += word_count
        else:
            # If the word limit is exceeded, finalize the current chunk and start a new one
            items.append(' '.join(current_item).strip())
            current_item = [sentence]
            current_word_count = word_count

    # Append the last chunk if it contains text
    if current_item:
        items.append(' '.join(current_item).strip())

    return items

# Save the text chunks to a single JSON file
def save_items_to_single_json(items, output_file):
    # Create a list of dictionaries containing chunk IDs and their respective text
    items_list = [{"chunk_id": i+1, "chunk": item} for i, item in enumerate(items)]
    try:
        # Write all items to a single JSON file
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(items_list, file, ensure_ascii=False, indent=4)
    except IOError as e:
        # Handle file write errors
        print(f"Error saving to {output_file}: {e}")

def main():
    # Directory containing the PDF files to be processed
    pdf_directory = 'data/in_chunk_pdf'
    # Output file to save the processed chunks
    output_file = 'data/out_chunk_pdf/spec_chunks.json'
    # Create the output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Download necessary resources for sentence tokenization
    download_nltk_resources()
    
    all_text = ''
    # Iterate over all PDF files in the specified directory
    for filename in os.listdir(pdf_directory):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(pdf_directory, filename)
            # Extract text from the current PDF file
            text = extract_text_from_pdf(pdf_path)
            if text.strip():
                all_text += text + '\n'

    # If no text could be extracted from any PDF, print an error message and exit
    if not all_text.strip():
        print("No text could be extracted from any PDF in the directory.")
        return

    # Clean the extracted text to remove unnecessary whitespace
    cleaned_text = clean_text(all_text)
    # Split the cleaned text into chunks based on sentence count and word limit
    items = item_text_by_sentence(cleaned_text)
    
    # Save the chunks to a single JSON file
    save_items_to_single_json(items, output_file)

    # Print a success message with the number of chunks created
    print(f'PDFs have been divided into {len(items)} items and saved to "{output_file}".')

if __name__ == "__main__":
    main()
