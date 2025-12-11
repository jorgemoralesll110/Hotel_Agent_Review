from fastmcp import MCPTool
from textblob import TextBlob

class SentimentAnalyzer(MCPTool):

    def analyze_sentiment(self, text: str):
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity

        if polarity > 0.2:
            sentiment = "positive"
        elif polarity < -0.2:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        return {"sentiment": sentiment, "polarity": polarity}

tool = SentimentAnalyzer()


# TODO: mejorar usando OPENAI dentro del MCP


