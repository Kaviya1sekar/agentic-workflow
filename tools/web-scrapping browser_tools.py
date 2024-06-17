import os
from dotenv import load_dotenv
from textwrap import dedent
from playwright.sync_api import sync_playwright
from langchain.tools import tool
from langchain_community.document_transformers import Html2TextTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from crewai import Agent, Task
from langchain_openai import AzureChatOpenAI
from langchain_core.documents import Document

load_dotenv()

llm = AzureChatOpenAI(
		openai_api_version=os.environ.get("AZURE_OPENAI_VERSION"),
		azure_deployment=os.environ.get("AZURE_OPENAI_DEPLOYMENT"),
		azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
		api_key=os.environ.get("AZURE_OPENAI_KEY"),
		model="gpt-4"
	)


class BrowserTools:

    @tool("Scrape website content")
    def scrape_and_summarize_website(self, url):
        """Scrape and extract website content."""
        url = "https://www.portauthoritynsw.com.au/sydney-harbour/pilotage-navigation/daily-vessel-movements/"
        summaries = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)
            page.wait_for_timeout(5000)  # Wait for 5 seconds to complete the page load.
            
            result = page.content()
            metadata = {"source": url}
            loaded_data = [Document(page_content=result, metadata=metadata)]
            
            tt = Html2TextTransformer()
            docs = tt.transform_documents(loaded_data)
            
            ts = RecursiveCharacterTextSplitter(chunk_size=7000, chunk_overlap=0)
            fd = ts.split_documents(docs)
            
            browser.close()

        for chunk in fd:
            agent = Agent(
                role='Principal Researcher',
                goal='Do amazing researches and create report with logistic data.',
                backstory="You're a Principal Researcher at a big company and you need to do a research about Vessel schedules in a terminal station.",
                llm=llm,
                allow_delegation=False
            )
            
            task = Task(
                agent=agent,
                description=dedent(f"""
                Extract the following data in comma-separated format: 
                (Note: Include the headers as the first record)
                - Vessel Name
                - Vessel Type
                - Berthing schedule
                - Status
                Return only this, nothing else.
                
                CONTENT
                ----------
                {chunk}
                """)
            )
            
            summary = task.execute()
            summaries.append(summary)
        
        print("\n\n".join(summaries))

