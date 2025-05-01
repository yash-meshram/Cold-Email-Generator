# Cold Email Generator

## Overview

**Cold Email Generator** is an AI-powered application that automates the process of generating personalized cold emails for job applications. By leveraging advanced language models and vector databases, the app extracts job postings from career pages, matches your portfolio projects to required skills, and crafts tailored cold emails to maximize your outreach effectiveness.

> **Note:** This project uses the [Llama 3 8B Instant](https://ai.meta.com/llama/) model (`llama-3.1-8b-instant`) via Groq for all language generation and understanding tasks.

## Model Details

- **LLM Used:** [Llama 3 8B Instant](https://ai.meta.com/llama/) (`llama-3.1-8b-instant`)
- **Provider:** [Groq](https://console.groq.com/)
- The model is accessed through the `langchain_groq` integration in the code (see `chains.py`).

## Features

- **Automated Web Scraping:** Extracts job postings from provided URLs.
- **AI-Powered Email Generation:** Uses LLMs (via LangChain and Groq) to generate personalized cold emails.
- **Portfolio Matching:** Matches your portfolio projects to job requirements using a vector database (ChromaDB).
- **Streamlit Interface:** User-friendly web interface for input and results.
- **Customizable:** Easily update your portfolio and adapt to different job postings.

## How It Works

1. **Input a Job URL:** Enter the URL of a job posting or career page.
2. **Web Data Extraction:** The app scrapes and cleans the job data.
3. **Job Parsing:** Extracts structured job information (role, company, skills, etc.).
4. **Portfolio Query:** Finds your most relevant projects based on required skills.
5. **Cold Email Generation:** Crafts a personalized email referencing your experience and portfolio.
6. **Output:** The generated email is displayed for review and use.

## Project Structure

```
app/
  main.py           # Streamlit app entry point
  chains.py         # Core logic for web extraction, job parsing, and email generation
  portfolio.py      # Portfolio management and vector DB integration
  utils.py          # Text cleaning utilities
  resources/        # Resource files (e.g., portfolio CSV)
VectorDB/           # Persistent vector database storage
testing/            # Test scripts and sample data
NOTES.txt           # Project notes and technical explanations
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- [Streamlit](https://streamlit.io/)
- [LangChain](https://python.langchain.com/)
- [ChromaDB](https://www.trychroma.com/)
- [Groq API Key](https://console.groq.com/)
- Other dependencies: `pandas`, `python-dotenv`, `re`

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd Cold-Email-Generator
   ```

2. **Create and activate a virtual environment (optional but recommended):**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install streamlit langchain chromadb langchain_groq langchain_community pandas python-dotenv
   ```

4. **Set up environment variables:**
   - Copy `app/.env` and add your Groq API key:
     ```
     GROQ_API_KEY="your_groq_api_key"
     ```

5. **Prepare your portfolio:**
   - Update `app/resources/my_portfolio.csv` with your projects, tech stack, and links.

### Running the App

```bash
streamlit run app/main.py
```

Open the provided local URL in your browser to use the app.

## Usage

1. Enter the URL of a job posting.
2. Click **Submit**.
3. Review the generated cold email and copy it for your application.

## Environment Variables

- `GROQ_API_KEY`: Your Groq API key for LLM access.

## Notes

- The app uses ChromaDB for fast vector search and storage of your portfolio.
- The AI model is configured for professional, personalized cold email generation.
- For best results, keep your portfolio CSV up to date and relevant.

## License

[MIT License](LICENSE) (or specify your license)
