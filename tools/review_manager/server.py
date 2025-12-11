from fastmcp import MCPTool
import json
import os

class ReviewManager(MCPTool):
    def _init_(self):
        super()._init_()
        self.file_path = "data/reviews.json"
        if not os.path.exists(self.file_path):
            json.dump([], open(self.file_path, "w"))

    def save_review(self, review: str, response: str):
        reviews = json.load(open(self.file_path))
        reviews.append({"review": review, "response": response})
        json.dump(reviews, open(self.file_path, "w"), indent=2)
        return {"status": "saved"}

    def list_reviews(self):
        reviews = json.load(open(self.file_path))
        return reviews

tool = ReviewManager()