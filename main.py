from src import chunk_pdf
from src import call_api_req
from src import clean_req
from src import group_req
from src import chunk_req
from src import call_api_trip
from src import clean_trip
from src import csv_to_cypher

def main():

    # Step 1: Divide the input PDF into LLM-manageable chunks
    chunk_pdf.main()

    # Step 2: Make an API call for each chunk of the PDF to identify requirements
    call_api_req.main()

    # Step 3: Transform the API response into readable JSON
    clean_req.main()

    # Step 4: Extract the requirements only
    group_req.main()

    # Step 5: Split the requirements up for feeding back to the API
    chunk_req.main()

    # Step 6: Make an API call for each chunk of the requirements to transform them into RDF triples.
    call_api_trip.main()

    # Step 7: Clean RDF triples and convert to CSV.
    clean_trip.main()

    # Step 8: Transform RDF to cypher
    csv_to_cypher.main()


if __name__ == "__main__":
    main()