import streamlit as st
import requests
import os
import time  # Import time to handle API rate limits
import google.generativeai as genai
from newspaper import Article, Config
from dotenv import load_dotenv

# 1. Setup & API Configuration
load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
NEWS_KEY = os.getenv("NEWS_API_KEY")

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-2.5-flash-lite')

# Browser configuration to avoid being blocked by news sites
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
config = Config()
config.browser_user_agent = user_agent
config.request_timeout = 10

# 2. UI Layout
st.set_page_config(page_title="AI News Summarizer", page_icon="🗞️")
st.title("🗞️ Personalized News Summarizer")
st.markdown("Stay updated with AI-powered technical summaries.")

topic = st.sidebar.text_input("Enter Topic", placeholder="e.g. Saffron Farming, AI Trends")
num_articles = st.sidebar.slider("Number of articles", 1, 5, 3)

# 3. Helper Functions
def fetch_news(query):
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_KEY}&language=en&pageSize={num_articles}"
    try:
        response = requests.get(url)
        return response.json().get('articles', [])
    except Exception as e:
        st.error(f"Failed to fetch news: {e}")
        return []

def get_summary(url):
    try:
        article = Article(url, config=config) 
        article.download()
        article.parse()
        
        if not article.text:
            return "Article found, but no readable content was extracted (might be behind a paywall)."

        prompt = f"Summarize this news article in 3 clear bullet points:\n\n{article.text}"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # Check if the error is a rate limit (429)
        if "429" in str(e):
            return "⚠️ Rate limit reached. Please try fetching fewer articles or wait a moment."
        return f"Error: Could not access the article. (Details: {str(e)})"

# 4. Main App Logic
if st.button("Get My Daily Digest"):
    if not topic:
        st.warning("Please enter a topic first!")
    else:
        articles = fetch_news(topic)
        
        if not articles:
            st.error("No news found for that topic.")
        else:
            st.info(f"Processing {len(articles)} articles... Please wait.")
            
            for art in articles:
                with st.expander(f"📌 {art['title']}"):
                    st.write("**Summary:**")
                    
                    # Fetching the summary
                    summary = get_summary(art['url'])
                    st.write(summary)
                    st.write(f"[Read Full Article]({art['url']})")
                
                # CRITICAL: Wait 5 seconds between articles to stay within Gemini Free Tier limits
                time.sleep(10) 
            
            st.success("Done! Your digest is ready.")
