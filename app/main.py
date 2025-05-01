import streamlit as st 
from portfolio import Portfolio
from chains import Chain

def create_streamlit_app(title):
    st.title(title)
    web_url = st.text_input(
        "Enter URL:",
        value = "https://careers.nike.com/analyst-ii-marketing-measurement/job/R-58710"
    )
    submit_btn = st.button('Submit')
    
    if True:
        # initializing vector db
        portfolio = Portfolio()

        # initializing llm model
        chain = Chain()

        # insert the data from csv to --> vector db
        portfolio.load_portfolio("app/resources/my_portfolio.csv")

        # extracting data from web_url
        webpage_data = chain.extract_webdata(web_url)

        # extract jobs from webpage_data
        jobs = chain.extract_jobs(webpage_data)

        # for each job in jobs generate a cold email
        for job in jobs:
            skills = job.get('skills', [])
            links = portfolio.query_link(skills)
            email = chain.generate_cold_email(job, links)
            st.code(email, language = 'markdown')
            

if __name__ == "__main__":
    title = "Cold Email Generator"
    create_streamlit_app(title)


# st.title("Cold Email Generator!")

# url_input = st.text_input(
#     "Enter URL:",
#     value = "https://careers.nike.com/analyst-ii-marketing-measurement/job/R-58710"
# )

# submit_btn = st.button("Submit")

# if submit_btn:
#     st.code("---Response will be here---")