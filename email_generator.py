from langchain_groq import ChatGroq

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.0,
    groq_api_key = "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"
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

result = chain_extract.invoke(
    input = {'page_data': page_data}
)
print(result.content)
