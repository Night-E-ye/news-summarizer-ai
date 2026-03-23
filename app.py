import streamlit as st
import requests
import os
import google.generativeai as genai
from newspaper import Article
from dotenv import load_dotenv

# 1. Setup
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel('gemini-2.5-flash')

# 2. UI Layout
st.set_page_config(page_title="AI News Summarizer", page_icon="🗞️")
st.title("🗞️ Personalized News Summarizer")
topic = st.sidebar.text_input("Enter Topic")
num_articles = st.sidebar.slider("Number of articles", 1, 5, 3)

# 3. Functions
def fetch_news(query):
    api_key = os.getenv("NEWS_API_KEY")
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={api_key}&language=en&pageSize={num_articles}"
    return requests.get(url).json().get('articles', [])

from newspaper import Article, Config  # Add Config here

# 1. Create a Browser User-Agent config
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
config = Config()
config.browser_user_agent = user_agent
config.request_timeout = 10

# 2. Update the get_summary function
def get_summary(url):
    try:
        # Pass the config here to look like a real browser
        article = Article(url, config=config) 
        article.download()
        article.parse()
        
        # Check if we actually got text
        if not article.text:
            return "Article found, but no readable content was extracted (might be behind a paywall)."

        prompt = f"Summarize this news article in 3 clear bullet points:\n\n{article.text}"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: Could not access the article. (Details: {str(e)})"
   

# 4. Main App Logic
if st.button("Get My Daily Digest"):
    articles = fetch_news(topic)
    if not articles:
        st.error("No news found for that topic.")
    else:
        for art in articles:
            with st.expander(f"📌 {art['title']}"):
                st.write("**Summary:**")
                summary = get_summary(art['url'])
                st.write(summary)
                st.write(f"[Read Full Article]({art['url']})")