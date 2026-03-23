# Personalized News Summarizer AI

A web application that fetches top headlines for a given topic using NewsAPI, scrapes the article content, and summarizes it into 3 clear bullet points using Google's Gemini API. The interface is built with Streamlit.

## Features
- Search for news articles by topic.
- Fetches article content from the web automatically.
- Provides a concise 3-bullet point summary using AI.
- Clean and interactive Streamlit UI.

## Setup Instructions

1. **Clone the repository or navigate to this folder.**
2. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Get API Keys:**
   - [NewsAPI Key](https://newsapi.org/)
   - [Google Gemini API Key](https://aistudio.google.com/app/apikey)
4. **Environment Variables:**
   - Create a `.env` file in this directory with the following variables:
     ```env
     NEWS_API_KEY=your_newsapi_key_here
     GEMINI_API_KEY=your_gemini_api_key_here
     ```
   - Alternatively, you can input the keys directly in the Streamlit app's sidebar.
5. **Run the App:**
   ```bash
   streamlit run app.py
   ```
