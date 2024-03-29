#!/usr/bin/env python3
"""8-all.py"""

def list_all(mongo_collection):
    """function that lists all documents in a collection"""

    # Initialize an empty list to store documents
    all_documents = []
    
    # Retrieve all documents from the collection
    cursor = mongo_collection.find({})
    
    # Iterate over the cursor and append documents to the list
    for document in cursor:
        all_documents.append(document)
    
    # Return the list of documents
    return all_documents

