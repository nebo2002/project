import streamlit as st
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd

# Download NLTK data (if not already downloaded)
# nltk.download("vader_lexicon")

# Create SentimentIntensityAnalyzer object
analyzer = SentimentIntensityAnalyzer()

# Function to perform sentiment analysis
def get_sentiment_score(text):
    sentiment_score = analyzer.polarity_scores(text)['compound']
    return sentiment_score

# Function to find a relevant product answer based on sentiment
def get_product_answer(user_input):
    sentiment_score = get_sentiment_score(user_input)
    if sentiment_score >= 0.05:
        return "Thank you for your positive feedback! We're glad you like our products."
    elif sentiment_score <= -0.05:
        return "We apologize for any inconvenience you experienced. Please contact our customer support for assistance."
    else:
        return "We appreciate your feedback. Let us know if you have any specific questions about our products."

# Function to search for relevant product information
def search_product_info(user_input):
    # Load Amazon product data (replace 'path/to/amazon_product_data.csv' with your actual file path)
    amazon_product_data = pd.read_csv('details.csv')
    relevant_product_info = amazon_product_data[amazon_product_data['name'].str.contains(user_input, case=False)]
    return relevant_product_info

# Streamlit app with SessionState
class SessionState:
    def __init__(self):
        self.user_input = None

state = SessionState()

def main():
    st.title("Amazon Product Chatbot")

    st.write("Chatbot: Hi! How can I assist you with our Amazon products today?")

    # Get user input with unique key
    user_input = st.text_input("You:", key="user_input").strip().lower()

    # Store user input in SessionState
    state.user_input = user_input

    if user_input == "exit":
        st.write("Chatbot: Goodbye! Have a great day.")
    else:
        # Search for relevant product information in the product data
        product_info = search_product_info(state.user_input)

        if not product_info.empty:
            st.write("Chatbot: Here's some information about the product:")
            st.table(product_info[['name', 'ratings','actual_price','discount_price']])
        else:
            # If no relevant product found, use sentiment analysis to provide an answer
            chatbot_response = get_product_answer(state.user_input)
            st.write(f"Chatbot: {chatbot_response}")

if __name__ == "__main__":
    main()
