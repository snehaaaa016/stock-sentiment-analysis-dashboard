# Stock Sentiment Dashboard

A simple and interactive web app to track real-time stock prices and market sentiment from the latest news.


## Features

- Real-time hourly stock price data from Yahoo Finance  
- Interactive candlestick charts with a dark theme  
- Sentiment analysis of top 5 recent news headlines using VADER  
- Metrics for latest closing price, percentage change, and data points  
- Search for any stock ticker symbol  

## Requirements

- Python 3.7 or higher  
- NewsAPI key (free to get at [newsapi.org](https://newsapi.org/))


**##Install dependencies:**
pip install -r requirements.txt


##Create a .env file in the root folder and add your NewsAPI key:

NEWS_API_KEY=your_api_key_here

##Usage

-Run the app with:

streamlit run app.py


Enter a stock ticker symbol in the sidebar and click Get Data to view price charts and news sentiment.

-Built With:

Streamlit

Yahoo Finance (yfinance)

Plotly

VADER Sentiment

NewsAPI


