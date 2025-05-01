import chromadb

chroma_client = chromadb.Client()

# switch `create_collection` to `get_or_create_collection` to avoid creating a new collection every time
collection = chroma_client.get_or_create_collection("my_collection")

# switch `add` to `upsert` to avoid adding the same documents every time
collection.upsert(                                  
    documents = [
        "This is a document about New York.",
        "This is a document about New Delhi."
    ],
    ids = ["id1","id2"]
)

document = collection.get(
    ids = "id2"
)
document

all_documents = collection.get()
all_documents

result = collection.query(
    query_texts = ["Query about Chole Bature."],     # Chroma will embed this for you
    n_results = 2                                    # how many results to return
)
result

result = collection.query(
    query_texts = ["Query about White people."],     
    n_results = 2                                
)
result

collection.delete(ids = all_documents["ids"])
collection.get()

collection.upsert(                                  
    documents = [
        "This is a document about New York.",
        "This is a document about New Delhi."
    ],
    ids = ["id1","id2"],
    metadatas = [
        {"url": "https://en.wikipedia.org/wiki/New_York_City"},
        {"url": "https://en.wikipedia.org/wiki/New_Delhi"}
    ]
)

result = collection.query(
    query_texts = ["Query about Chole Bature."],     # Chroma will embed this for you
    n_results = 2                                    # how many results to return
)
result