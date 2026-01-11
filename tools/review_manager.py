import json
import os

FILE_PATH = "data/reviews.json"

def _init_storage():
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, "w") as f:
            json.dump([], f)

_init_storage()

def save_review(review: str, response: str):
    with open(FILE_PATH, "r") as f:
        reviews = json.load(f)

    reviews.append({
        "review": review,
        "response": response
    })

    with open(FILE_PATH, "w") as f:
        json.dump(reviews, f, indent=2)

    return {"status": "saved"}

def list_reviews():
    with open(FILE_PATH, "r") as f:
        return json.load(f)
