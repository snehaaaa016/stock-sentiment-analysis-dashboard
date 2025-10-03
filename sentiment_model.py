from textblob import TextBlob

def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0:
        return "Positive 😀"
    elif polarity < 0:
        return "Negative 😡"
    else:
        return "Neutral 😐"

if __name__ == "__main__":
    samples = [
        "Stock prices are going up fast!",
        "The market crashed badly today.",
        "Investors are waiting for updates."
    ]
    for s in samples:
        print(s, "->", analyze_sentiment(s))
