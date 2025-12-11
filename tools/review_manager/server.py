from fastmcp import MCPTool
import json
import os

class ReviewManager(MCPTool):

    def _init_(self):
        super()._init_()
        self.path = "data/reviews.json"
        if not os.path.exists("data"):
            os.makedirs("data")
        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                json.dump([], f)

    def save_review(self, review: str, response: str):
        with open(self.path, "r") as f:
            all_reviews = json.load(f)

        all_reviews.append({"review": review, "response": response})

        with open(self.path, "w") as f:
            json.dump(all_reviews, f, indent=2)

        return {"status": "saved"}

    def list_reviews(self):
        with open(self.path, "r") as f:
            return json.load(f)

tool = ReviewManager()