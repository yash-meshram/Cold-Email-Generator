from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

# loading .env file
load_dotenv(dotenv_path = "app\\.env")

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.0,
    api_key = os.getenv("GROQ_API_KEY")
)

from langchain_community.document_loaders import WebBaseLoader

loader = WebBaseLoader(
    web_path = "https://careers.nike.com/analyst-ii-marketing-measurement/job/R-58710"
)
print(loader)

docs = loader.load()
print(docs)

print(docs[0].metadata)

print(docs[0].page_content)
page_data = docs.pop().page_content
print(page_data)


from langchain_core.prompts import PromptTemplate

prompt_extract = PromptTemplate.from_template(
    """
    ### SCRAPED TEXT FROM WEBSITE:
    {page_data}
    ### INSTRUCTION:
    The scraped text is from the carrer's page of a website.
    Yor job is to extract the job postings and return them in valid JSON format containing following keys:
    `company`, `role`, `experience`, `skills` and `description`.
    Only return the valid JSON.
    ### VALID JSON (NO PREAMBLE):
    """
)

# passing the prompt to model
chain_extract = prompt_extract | llm

response = chain_extract.invoke(
    input = {'page_data': page_data}
)
print(response)
print(response.content)
type(response.content) 

from langchain_core.output_parsers import JsonOutputParser

json_parser = JsonOutputParser()
json_response = json_parser.parse(response.content)
json_response
type(json_response)

JsonOutputParser().parse(response.content)

# next step: Prepared vector database (chromadb)
# ---------------------------------------------------

import pandas as pd

df = pd.read_csv("my_portfolio.csv")
df

import chromadb

client = chromadb.PersistentClient("vector_store")              # this create the chromadb in disk - we will be able to see it 
collection = client.get_or_create_collection(name = 'portfolio')
# for row in range(0, df.shape[0]):
#     collection.upsert(
#         documents = df.iloc[row]['Techstack'],
#         metadatas = {'url': df.iloc[row]['Links']},
#         ids = 'id' + str(row+1)
#     )

for index, row in df.iterrows():
    collection.upsert(
        documents = row['Techstack'],
        metadatas = {'url': row['Links']},
        ids = 'id' + str(index + 1)
    )
    
# all skills (techstack) and project (url)
collection.get()   
collection.get(ids = 'id6')

# get data for python and sql skills (techstack)
collection.query(
    query_texts = [
        "Experience in Python",
        "Experience in SQL"
    ],
    n_results = 2
).get('metadatas')

# in job post what skills are required
job = json_response
job['skills']['required']
job.get('skills', [])['required']
job.get('skills', [])

# search this skills in collection
link_list = collection.query(
    query_texts = job['skills']['required'],
    n_results = 2
).get('metadatas', [])
link_list

# Generate email
# -----------------------

prompt_extract = PromptTemplate.from_template(
    """
    ### JOB DESCRIPTION:
    {job_description}
    
    ### INSTRUCTIONS:
    You are Yash, working as Technical Lead in HCLTech from past 2.5 years.
    In your job yo had worked on the following technologies: .Net, Angular, SQL, Azure, C# (language)
    In your personal project (not in company, your personal) you had worked on following technologies: 
        languages: python
        Data: SQL, Chroma (Vector database)
        Machine Learning: sklearn
        visualization: matplotlib, seaborn, plotly
        Dashboard: Power BI, tableau
        Neural Network: tensorflow
        GenAi: langchain, LLM
    Your job is to write a cold email to the client regarding the job mentioned and how you will be a good fit for it.
    Also add the most relevant projects from the following list: {link_list}.
    Remember you are Yash.
    Do not provide pereamble.
    
    ### EMAIL (NO PREAMBLE):
    """
)

# passing the prompt to model
chain_extract = prompt_extract | llm

response = chain_extract.invoke(
    input = {
        'job_description': json_response,
        'link_list': link_list
    }
)
print(response.content)