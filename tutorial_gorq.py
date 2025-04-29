from langchain_groq import ChatGroq

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.0,
    groq_api_key = "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"
)

response = llm.invoke("First persone to step foot on moon...")
print(response)
print("\n", response.content)

