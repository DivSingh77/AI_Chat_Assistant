import random

import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Load dataset
df = pd.read_csv("backend/dataset/train.csv")

class QueryRequest(BaseModel):
    question: str

@app.post("/query")
async def query_data(request: QueryRequest):
    question = request.question.lower()
    
    if "percentage of passengers were male" in question:
        male_percentage = (df["Sex"].value_counts()["male"] / len(df)) * 100
        return {"response": f"🧑 The percentage of male passengers: {male_percentage:.2f}%"}
    
    elif "histogram of passenger ages" in question:
        return {"response": "📊 Check the visualization section in Streamlit!"}
    
    elif "average ticket fare" in question:
        avg_fare = df["Fare"].mean()
        return {"response": f"🎟️ The average ticket fare was ${avg_fare:.2f}"}
    
    elif "passengers embarked from each port" in question:
        embark_counts = df["Embarked"].value_counts().to_dict()
        return {"response": embark_counts}
    
    elif "survival rate by class" in question:
        survival_rates = df.groupby("Pclass")["Survived"].mean().to_dict()
        return {"response": survival_rates}
    
    elif "youngest passenger" in question:
        youngest = df["Age"].min()
        return {"response": f"👶 The youngest passenger was {int(youngest)} years old!"}
    
    elif "most expensive ticket price" in question:
        max_fare = df["Fare"].max()
        return {"response": f"💰 The most expensive ticket was ${max_fare:.2f}!"}
    
    else:
        return {"response": "🤖 Sorry, I don't have an answer for that. Try rephrasing!"}
