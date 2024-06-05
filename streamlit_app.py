import streamlit as st
import pymongo
from langchain_community.llms import Ollama
import os
import time
from datetime import datetime
import pandas as pd

# Initialize Ollama model
llm = Ollama(model="llama2")

# Function to save chat to MongoDB along with time taken and date of generating
def save_chat(user_query, response, time_taken):
    client = pymongo.MongoClient("mongodb://localhost:27017/")  # Connect to MongoDB
    db = client["jamalchat"]  # Create or connect to the "jamalchat" database
    collection = db["chats"]  # Access or create the "chats" collection
    date_generated = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    chat = {"User Query": user_query, "Response": response, "Time Taken (seconds)": time_taken, "Date Generated": date_generated}
    collection.insert_one(chat)  # Insert the chat document into the collection

# Function to load saved chats from MongoDB and sort by "Date Generated" in descending order
def load_chats():
    client = pymongo.MongoClient("mongodb://localhost:27017/")  # Connect to MongoDB
    db = client["jamalchat"]  # Connect to the "jamalchat" database
    collection = db["chats"]  # Access the "chats" collection
    return list(collection.find().sort("Date Generated", pymongo.DESCENDING))  # Retrieve and sort all documents from the collection

# Streamlit UI
st.title("StockSenseChat")

# User input for query
user_query = st.text_input("Enter your query")

# Button to trigger response generation
if st.button("Generate"):
    start_time = time.time()  # Start time for response generation
    # Generating response using Ollama model
    response = llm.invoke(user_query)
    end_time = time.time()  # End time for response generation
    time_taken = end_time - start_time  # Calculate time taken
    # Saving chat to MongoDB
    save_chat(user_query, response, time_taken)
    # Displaying response
    st.write("Here's your answer:")
    st.write(response)
    st.write(f"Time taken: {time_taken} seconds")

# Show saved chats button
if st.button("Show Saved Chats"):
    # Load saved chats from MongoDB and sort by "Date Generated" in descending order
    chats = load_chats()
    # Convert chats to DataFrame for display
    df = pd.DataFrame(chats)
    # Display saved chats in a table
    st.subheader("Saved Chats")
    st.dataframe(df)
