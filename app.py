import os
import streamlit as st
import yfinance as yf
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from dotenv import load_dotenv
from requests.utils import quote
import plotly.graph_objects as go

# -----------------------
# Page config and Dark Mode CSS
# -----------------------
st.set_page_config(page_title="Stock Sentiment Dashboard", layout="wide", initial_sidebar_state="expanded")

dark_mode_css = """
<style>
body, .main, .css-1d391kg, .css-1d391kg div {
    background-color: #0e1117 !important;
    color: #cdd6f4 !important;
}
h1, h2, h3, h4, h5 {
    color: #89b4fa !important;
}
input, textarea, button {
    background-color: #1e2130 !important;
    color: #cdd6f4 !important;
    border-color: #2f333d !important;
}
.css-1v3fvcr {
    color: #cdd6f4 !important;
    background-color: #0e1117 !important;
}
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}
::-webkit-scrollbar-thumb {
    background-color: #313244;
    border-radius: 4px;
}
</style>
"""
st.markdown(dark_mode_css, unsafe_allow_html=True)

# -----------------------
# Load API Key from .env
# -----------------------
load_dotenv()
API_KEY = os.getenv("NEWS_API_KEY")

# -----------------------
# Sentiment Analysis (VADER)
# -----------------------
analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    scores = analyzer.polarity_scores(text)
    if scores['compound'] > 0.05:
        return "Positive 😀"
    elif scores['compound'] < -0.05:
        return "Negative 😡"
    else:
        return "Neutral 😐"

# -----------------------
# Fetch News Headlines
# -----------------------
def fetch_news(ticker, api_key):
    query = quote(ticker)
    url = f"https://newsapi.org/v2/everything?q={query}&language=en&sortBy=publishedAt&apiKey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        return []
    data = response.json()
    if data.get("status") == "ok":
        return [article["title"] for article in data["articles"][:5]]
    return []

# -----------------------
# Plot Candlestick Chart
# -----------------------
def plot_candlestick(df):
    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        increasing_line_color='#0fbcf9',
        decreasing_line_color='#f31260',
    )])
    fig.update_layout(
        paper_bgcolor='#0e1117',
        plot_bgcolor='#0e1117',
        font_color='#cdd6f4',
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis_rangeslider_visible=False,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#222430')
    )
    return fig

# -----------------------
# Format ticker based on selected exchange
# -----------------------
def format_ticker(ticker, exchange):
    ticker = ticker.strip().upper()
    if exchange == "NSE" and not ticker.endswith(".NS"):
        ticker += ".NS"
    elif exchange == "BSE" and not ticker.endswith(".BO"):
        ticker += ".BO"
    # Global stocks have no suffix
    return ticker

# -----------------------
# Streamlit App Layout
# -----------------------
st.title("📈 Real-Time Stock Market Sentiment Dashboard with News")

with st.sidebar:
    st.header("Settings")
    raw_ticker = st.text_input("Enter stock ticker symbol:", value="RELIANCE")
    exchange = st.selectbox("Select Exchange:", ["NSE", "BSE", "Global (no suffix)"])
    st.markdown("⚠️ NSE and BSE tickers will automatically get `.NS` or `.BO` suffix respectively.")
    get_data = st.button("Get Data")

if get_data:
    ticker = format_ticker(raw_ticker, exchange)
    with st.spinner(f"Fetching stock data and news for {ticker}..."):
        data = yf.download(ticker, period="5d", interval="1h")

        if not data.empty:
            # Remove timezone info to fix Plotly candlestick display issue
            data.index = data.index.tz_localize(None)

            # Fix multi-index columns to simple columns
            data.columns = data.columns.get_level_values(0)

    if data.empty:
        st.error(f"No data found for ticker '{ticker}'. Please check the symbol and exchange.")
    else:
        latest_close = float(data["Close"].iloc[-1])
        previous_close = float(data["Close"].iloc[-2]) if len(data) > 1 else latest_close
        change = latest_close - previous_close
        pct_change = (change / previous_close) * 100 if previous_close != 0 else 0

        col1, col2, col3 = st.columns(3)
        col1.metric("Latest Close Price", f"${latest_close:.2f}", delta=f"{change:.2f}")
        col2.metric("Percentage Change", f"{pct_change:.2f}%", delta_color="inverse" if pct_change < 0 else "normal")
        col3.metric("Data Points", len(data))

        st.subheader(f"Candlestick Chart for {ticker}")
        fig = plot_candlestick(data)
        st.plotly_chart(fig, use_container_width=True)

        with st.expander("Show raw data"):
            st.dataframe(data.tail(10))

        if API_KEY:
            headlines = fetch_news(ticker, API_KEY)
            if headlines:
                st.subheader("Latest Financial News & Sentiment")
                sentiments = [analyze_sentiment(h) for h in headlines]
                for headline, sentiment in zip(headlines, sentiments):
                    st.markdown(f"📰 **{headline}**  →  {sentiment}")

                pos = sentiments.count("Positive 😀")
                neg = sentiments.count("Negative 😡")
                neu = sentiments.count("Neutral 😐")
                st.markdown(f"**Overall Sentiment:** 👍 {pos} | 👎 {neg} | 😐 {neu}")
            else:
                st.warning("No news found for this ticker.")
        else:
            st.error("❌ No API key found. Please add NEWS_API_KEY in your .env file.")
