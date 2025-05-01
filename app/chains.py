import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
import utils

# loading .env file
load_dotenv(dotenv_path = "app\\.env")

class Chain:
    def __init__(self):
        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0.0,
            api_key = os.getenv("GROQ_API_KEY")
        )
        
    # extract data from web page
    def extract_webdata(self, web_url):
        loader = WebBaseLoader(
            web_path = web_url
        )
        webpage_data = loader.load().pop().page_content
        webpage_data = utils.clean_text(webpage_data)
        return webpage_data
        
    # analyze the webpage_data --> job data in json formate
    def extract_jobs(self, webpage_data):
        # write a prompt
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            # {page_data}
            ### INSTRUCTION:
            The scraped text is from the carrer's page of a website.
            Yor job is to extract the job postings and return them in valid JSON format containing following keys:
            `company`, `role`, `experience`, `skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        # passing the prompt to llm model
        chain_extract = prompt_extract | self.llm   
        # excute and get response        
        response = chain_extract.invoke(                       
            input = {'page_data': webpage_data}
        )
        # convert the response into JSON
        try: 
            json_parser = JsonOutputParser()
            json_res = json_parser.parse(response.content)
        except OutputParserException:
            raise OutputParserException("content too big. Unable to parse json.")
        
        return json_res if isinstance(json_res, list) else [json_res]
    
    # generate cold email
    def generate_cold_email(self, json_res, link_list):
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
        
        chain_extract = prompt_extract | self.llm
        
        res = chain_extract.invoke(
            input = {
                "job_description": json_res,
                "link_list": link_list
            }
        )
        return res.content
        
if __name__ == "__main__":
    print(os.getcwd())
    print(os.getenv("GROQ_API_KEY"))       
        
        
        
        