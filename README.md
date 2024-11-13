# Reqify

Takes a long-form PDF document and uses OpenAI models to automatically extract individual requirement statements, turn them into semantic triples, and turn those triples into cypher. AKA turns a document into a model of a document.

> IMPORTANT: You need an API key from OpenAI for this script to work. A Neo4J graph database is used to visualize and interact with the triples.

## Why?

Product teams typically ingest requirements documents through reading them and meeting to discuss ambiguities and completeness. This process can take weeks or months depending on the complexity of the document and the project. Documents are also not model-based. If you want to reference them, you have to manually find the part of the document you want to reference, which requires repeated re-reading. Often, there is missing context that requires more look ups and re-reading. In academia, for example, recursive referencing leads the reader to spend large amounts of time trying to find the original source of information that is re-referenced along a chain of multiple papers.

It is difficult for computers to assist in document analysis. Feed a Large Language Model (LLM) a long, complex document and it will do what a human does, briefly scanning over some of it to try and come up with an answer that sounds good, rendering the document less useful than intended or, in some cases, useless. LLMs do not currently do well at ingesting a large document and fully understanding it. Their analysis tends to be lazy and hallucinatory.

Complex product design documents should be engineered first as model-based data artifacts so that computers can assist with truly integrating them into the development of a product. Because they are often written document-first, this script reverse engineers a document to a proof of concept for what could be a new foundation for future design documentation: a simplified, straight-to-the-point knowledge graph.

In the absence of a model-first approach to design documentation, an alternative may be to transform the document to a model and then re-engineer it to a better, more efficient document. Modern long-form requirements specifications are plagued with superfluous, redundant, ambiguous, and, on some occasions, even contradictory language.

## Model-Based Documentation Use Cases

- Models make it harder for an AI to be lazy or hallucinate because they reduce the obstacles between the query and the answer.
- Models can clearly define a path between a query and an accurate answer.
- Models make it easier to govern document consistency (i.e. graph schema that governs new and existing triples).
- Semantic triples are easier for humans to understand.
- Discover emergent interdependencies and hierarchies prior to drafting the document rather than after analyzing it.
- Establish traceability between elements early.
- Reference specific parts of the model in other software to provide verification and validation of concepts.
- Attach metadata to elements of a triple (i.e. properties in Neo4J) to add even more information density per triple.
- Models can be versioned.
- Models can have metadata added to them at anytime (i.e. user comments and revision requests on model elements).

## How It Works

1) Takes an input of any PDF document.
2) Breaks the document down into chunks that are manageable for modern LLM attention spans.
3) For each chunk, the OpenAI API is called and a model is instructed to analyze the chunk for requirement statements.
4) The model sends a response with all the requirement statements it finds in a chunk.
5) Those requirement statements are then sent back through the API and now the model is asked to break them down into semantic triples.
6) The script converts the triples to cypher statements, effectively breaking down sentences to their most basic, atomic form.

From there, you can paste the cypher into Neo4J to visualize the way that the triples relate to each other and do all sorts of other fun data science things.

## Setup

1) Clone this repo.
2) Navigate to the project directory in terminal
3) Set up a Python virtual environment
4) Install dependencies from *requirements.txt*

## Usage

> IMPORTANT: You need an API key from OpenAI for this program to work.

1) Stick the document want to analyze in data/in_chunk_pdf
2) Create a file in the main directory of the repo called `api-key.env`
3) In the `api-key.env` file, paste: `API_KEY="YOUR OPENAI API KEY"`
4) Replace `YOUR OPENAI API KEY` with your actual OpenAI API Key and save the file. Keep the quotes around the key.
5) Run `main.py`.
6) Copy and paste the cypher into your Neo4J graph database and use Bloom to look at how interconnected the ideas in the document are.

## Additional Information

- `src` is the folder location of the components that main calls.
- script inputs and outputs are in the `data` folder of the repo.

## Results

GPT-4o performed better than GPT-4o-mini as was expected. Competitor models have not been tested yet. This script doesn't read pictures. It just skips over them, so some knowledge may be missed. There is still some significant work to be done in the area of prompt engineering to get better results from the LLM, but it is clearly capable of extracting requirements and transforming them into model-able elements such as semantic triples. For better LLM performance, try reducing the token size of its API inputs and experimenting with different variations of the prompts.
