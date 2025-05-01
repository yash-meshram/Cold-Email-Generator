import pandas as pd
import chromadb

class Portfolio:
    def __init__(self):
        self.client = chromadb.PersistentClient("VectorDB")
        self.collection = self.client.get_or_create_collection(name = "portfolio")
        
    # Load the portfolio = entering data in vector db (chromadb)
    def load_portfolio(self, file_path):
        file_path = file_path
        df = pd.read_csv(file_path)
        for index, row in df.iterrows():
            self.collection.upsert(
                documents = row['Techstack'],
                metadatas = {'url': row['Links']},
                ids = 'id' + str(index + 1)
            )
    
    # get the urls for the given specific skills
    def query_link(self, skills):
        link_list = self.collection.query(
            query_texts = skills,
            n_results = 2
        ).get('metadatas', [])
        return link_list