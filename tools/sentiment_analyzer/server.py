from fastmcp import MCPTool
import textblob

class SentimentAnalyzer(MCPTool):

    def analyze_sentiment(self, text: str):
        blob = textblob.TextBlob(text)
        polarity = blob.sentiment.polarity
        sentiment = (
            "positive" if polarity > 0.2 else
            "negative" if polarity < -0.2 else
            "neutral"
        )
        return {"sentiment": sentiment, "polarity": polarity}

tool = SentimentAnalyzer()


# TODO: mejorar usando OPENAI dentro del MCP


