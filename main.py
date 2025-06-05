import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variable
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise ValueError("API_KEY not found. Please set it in the .env file.")

genai.configure(api_key=API_KEY)

# Initialize the model
model = genai.GenerativeModel("gemini-1.5-flash-latest")

def chat():
    print("💬 Gemini Chatbot (type 'exit' to quit)")
    conversation = model.start_chat()

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("👋 Goodbye!")
            break

        response = conversation.send_message(user_input)
        print("Gemini:", response.text)

if __name__ == "__main__":
    chat()
