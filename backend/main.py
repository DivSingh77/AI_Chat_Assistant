from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd

app = FastAPI()

# Load the Titanic dataset
train_df = pd.read_csv("backend/dataset/train.csv")
test_df = pd.read_csv("backend/dataset/test.csv")

class QueryRequest(BaseModel):
    question: str

@app.get("/")
def home():
    return {"message": "Titanic Chatbot API is running with custom dataset!"}

@app.post("/query")
def query_data(request: QueryRequest):
    question = request.question.lower()

    if "percentage of passengers were male" in question:
        male_percentage = train_df['Sex'].value_counts(normalize=True)['male'] * 100
        return {"response": f"{male_percentage:.2f}% of the passengers were male."}

    elif "histogram of passenger ages" in question:
        return {"response": "Please generate a histogram using the frontend."}

    elif "average ticket fare" in question:
        avg_fare = train_df["Fare"].mean()
        return {"response": f"The average ticket fare was ${avg_fare:.2f}."}

    elif "passengers embarked from each port" in question:
        embark_counts = train_df["Embarked"].value_counts().to_dict()
        return {"response": embark_counts}

    else:
        return {"response": "I couldn't understand your question. Please try again!"}
