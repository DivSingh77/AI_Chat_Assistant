import random

import matplotlib.pyplot as plt
import pandas as pd
import requests
import seaborn as sns
import streamlit as st

# Load dataset
train_df = pd.read_csv("backend/dataset/train.csv")

# Streamlit UI Improvements
st.set_page_config(page_title="Titanic Dataset Chatbot", layout="wide")

# Custom Styling
st.markdown("""
    <style>
        .main {background-color: #f4f4f4;}
        .stTextInput {border-radius: 10px;}
        .stButton > button {border-radius: 10px; font-size: 16px; background-color: #ff4b4b; color: white;}
        .stMarkdown {font-size: 18px; font-weight: bold;}
    </style>
""", unsafe_allow_html=True)

st.title("🚢 Titanic Dataset Chatbot")
st.write("Ask any question related to the Titanic dataset and get insights instantly!")

# Suggested Questions Dropdown
questions = [
    "What percentage of passengers were male on the Titanic?",
    "Show me a histogram of passenger ages",
    "What was the average ticket fare?",
    "How many passengers embarked from each port?",
    "What is the survival rate by class?",
    "Who was the youngest passenger?",
    "What was the most expensive ticket price?"
]
selected_question = st.selectbox("💡 Suggested Questions", ["Select a question..."] + questions)

# User Input
question = st.text_input("Type your own question:", value=selected_question if selected_question != "Select a question..." else "")

if st.button("Ask Chatbot"):
    if question.strip():
        response = requests.post("http://127.0.0.1:8000/query", json={"question": question})
        data = response.json()
        st.success("🤖 Chatbot: " + data["response"])
    else:
        st.warning("Please enter a valid question!")

# Visualization Options
st.sidebar.header("📊 Visualization Options")
viz_options = ["Histogram of Passenger Ages", "Survival Rate by Class", "Embarkation Count", "Random Fun Fact"]
selected_viz = st.sidebar.radio("Choose a Visualization:", viz_options)

fig, ax = plt.subplots(figsize=(6, 4))

if selected_viz == "Histogram of Passenger Ages":
    st.subheader("📌 Histogram of Passenger Ages")
    sns.histplot(train_df["Age"].dropna(), bins=20, kde=True, ax=ax)
    st.pyplot(fig)

elif selected_viz == "Survival Rate by Class":
    st.subheader("📌 Survival Rate by Class")
    survival_rates = train_df.groupby("Pclass")["Survived"].mean()
    survival_rates.plot(kind="bar", color=['#ff4b4b', '#4bafff', '#4bff88'], ax=ax)
    st.pyplot(fig)

elif selected_viz == "Embarkation Count":
    st.subheader("📌 Embarkation Count")
    train_df["Embarked"].value_counts().plot(kind="bar", color=['#ffa500', '#4bafff', '#ff4b4b'], ax=ax)
    st.pyplot(fig)

elif selected_viz == "Random Fun Fact":
    fun_facts = [
        f"🎟️ The most expensive ticket was ${train_df['Fare'].max():.2f}!",
        f"👶 The youngest passenger was {int(train_df['Age'].min())} years old!",
        f"🛳️ The Titanic had {train_df.shape[0]} passengers in the dataset!"
    ]
    st.subheader("🎉 Random Fun Fact")
    st.write(random.choice(fun_facts))

st.write("\n---\n🚀 **Powered by FastAPI & Streamlit**")
