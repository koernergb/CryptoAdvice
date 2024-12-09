import asyncio
from crawl4ai import AsyncWebCrawler
import logging
from groq import Groq
import streamlit as st
import re
import os
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CryptoAnalyzer:
   def __init__(self):
       self.groq_client = Groq(
           api_key=os.environ["GROQ_API_KEY"]
       )

   def filter_content(self, content):
       """Filter content to include only latest crypto news section"""
       start_marker = "# Latest Crypto News"
       end_marker = "ABOUT"
       
       try:
           start_idx = content.find(start_marker)
           end_idx = content.find(end_marker)
           
           if start_idx != -1 and end_idx != -1:
               filtered_content = content[start_idx:end_idx].strip()
               filtered_content = re.sub(r'\[!\[.*?\]\(.*?\)\]', '', filtered_content)
               filtered_content = re.sub(r'\[.*?\]\(.*?\)', '', filtered_content)
               filtered_content = re.sub(r'!\[.*?\]\(.*?\)', '', filtered_content)
               filtered_content = re.sub(r'\n\s*\n+', '\n\n', filtered_content)
               return filtered_content
           return content
       except Exception as e:
           logger.error(f"Error filtering content: {str(e)}")
           return content

   def analyze_with_groq(self, content):
       """Analyze scraped content using Groq LLM"""
       system_prompt = """You are a cryptocurrency market analyst. Analyze the provided news content and:
       1. Identify key market signals (bullish/bearish)
       2. Provide specific asset allocation advice  
       3. Highlight any significant risks or opportunities
       4. Give actionable recommendations
       
       Format your response as a structured analysis with clear sections."""

       augmented_query = f"Based on this recent crypto news, provide market analysis and recommendations:\n\n{content}"

       try:
           chat_completion = self.groq_client.chat.completions.create(
               model="llama-3.1-70b-versatile",
               messages=[
                   {"role": "system", "content": system_prompt},
                   {"role": "user", "content": augmented_query}
               ]
           )
           return chat_completion.choices[0].message.content
       except Exception as e:
           logger.error(f"Error analyzing with Groq: {str(e)}")
           return None

   async def scrape_and_analyze(self):
       """Scrape and analyze CoinDesk news"""
       url = "https://www.coindesk.com/latest-crypto-news"
       
       async with AsyncWebCrawler(
           verbose=True,
           wait_for_selector="article",
           timeout=30,
           use_browser=True
       ) as crawler:
           try:
               with st.spinner('Fetching latest crypto news...'):
                   result = await crawler.arun(
                       url=url,
                       clean_tags=True,
                       extract_media=True
                   )
                   
               filtered_content = self.filter_content(result.markdown)
               
               with st.spinner('Analyzing market conditions...'):
                   analysis = self.analyze_with_groq(filtered_content)
               
               return filtered_content, analysis
               
           except Exception as e:
               logger.error(f"Error in scrape and analyze: {str(e)}")
               st.error(f"Error: {str(e)}")
               return None, None

def main():
   if "GROQ_API_KEY" not in os.environ:
       st.error("Please set the GROQ_API_KEY in environment variables")
       return

   st.set_page_config(page_title="Crypto Market Analyzer", page_icon="📈")
   
   st.title("Crypto Market Analyzer")
   st.markdown("---")

   analyzer = CryptoAnalyzer()

   if st.button("Analyze Latest Market News", type="primary"):
       try:
           loop = asyncio.get_event_loop()
       except RuntimeError:
           loop = asyncio.new_event_loop()
           asyncio.set_event_loop(loop)
       
       news, analysis = loop.run_until_complete(analyzer.scrape_and_analyze())

       if news and analysis:
           col1, col2 = st.columns(2)
           
           with col1:
               st.subheader("Latest Crypto News")
               st.text_area("", value=news, height=400, disabled=True)
               
           with col2:
               st.subheader("Market Analysis")
               st.markdown(analysis)

           st.markdown("---")
           st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    # Get port from environment variable (Render sets this)
    port = int(os.environ.get("PORT", "8501"))  # Default to 8501 if PORT not set
    st.set_page_config(page_title="Crypto Market Analyzer", page_icon="📈")
    main()
