from langchain_groq import ChatGroq

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.0,
    groq_api_key = ""
)

response = llm.invoke("First persone to step foot on moon...")
print(response)
print("\n", response.content)

