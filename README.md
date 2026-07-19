# 🏙️ City Intelligence System

An AI-powered conversational agent built with **LangChain**, **Mistral**, and **Streamlit** that can intelligently fetch real-time weather and the latest news for any city in the world.

## ✨ Features
- **Conversational UI**: A sleek, easy-to-use chat interface built with Streamlit.
- **Agentic Tool Calling**: Powered by the `mistral-medium-latest` model which autonomously decides when to use tools to accurately answer user queries.
- **Real-time Weather**: Integrates with the OpenWeatherMap API to get up-to-date weather conditions and temperatures (in Celsius).
- **Latest News**: Integrates with the Tavily Search API to find the most recent news articles and summaries for a given location.

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have Python installed, then install the required dependencies using the provided `requirements.txt`:
```bash
pip install -r requirements.txt
```
*(If you are using a virtual environment, ensure it is activated first).*

### 2. Environment Variables
Create a `.env` file in the root of the project to securely store your API keys. You will need to add:
```env
MISTRAL_API_KEY=your_mistral_api_key
TAVILY_API_KEY=your_tavily_api_key
```
*(Note: If you are using OpenWeatherMap, ensure your API key is correctly set in `Agent.py` or added to this `.env` file).*

### 3. Run the Application
**For the Web Interface (Recommended):**
To start the Streamlit conversational UI, run this command in your terminal:
```bash
python -m streamlit run app.py
```

**For the Terminal Interface:**
If you prefer a raw text interface with manual "human-in-the-loop" tool approvals, you can run the agent script directly:
```bash
python Agent.py
```

## 🛠️ Technologies Used
- [LangChain](https://python.langchain.com/) - LLM framework & tool orchestration
- [Mistral AI](https://mistral.ai/) - Large Language Model
- [Streamlit](https://streamlit.io/) - Web UI framework
- [Tavily Search](https://tavily.com/) - AI search engine for news
- [OpenWeatherMap](https://openweathermap.org/) - Weather API
