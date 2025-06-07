import os
import json
import random
import pickle
import numpy as np
import nltk
import requests
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
from .extensions import db
from .models import ChatbotInteraction, User
from flask_login import current_user
from datetime import datetime
from bs4 import BeautifulSoup
from flask import Blueprint, request, jsonify


lemmatizer = WordNetLemmatizer()

# Load intents
INTENTS_PATH = os.path.join(os.path.dirname(__file__), 'intents.json')
with open(INTENTS_PATH, 'r') as file:
    intents = json.load(file)

# Paths for model and data
MODEL_FILE = os.path.join(os.path.dirname(__file__), 'chatbot_model.h5')
WORDS_FILE = os.path.join(os.path.dirname(__file__), 'words.pkl')
CLASSES_FILE = os.path.join(os.path.dirname(__file__), 'classes.pkl')

# Load data
words = pickle.load(open(WORDS_FILE, 'rb'))
classes = pickle.load(open(CLASSES_FILE, 'rb'))

# Helper functions
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence.lower())
    return [lemmatizer.lemmatize(word) for word in sentence_words]

def bow(sentence, words):
    sentence_words = clean_up_sentence(sentence)
    return np.array([1 if w in sentence_words else 0 for w in words], dtype=np.float32)

# Function to log chatbot interaction
def log_chatbot_interaction(message, response):
    user = current_user if current_user.is_authenticated else None
    user_id = user.id if user else None

    interaction = ChatbotInteraction(
        message=message,
        response=response,
        user_id=user_id,
        timestamp=datetime.utcnow()
    )
    db.session.add(interaction)
    db.session.commit()

def get_url_summary(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        text = ' '.join([para.get_text() for para in paragraphs])
        return text[:500]  # Return first 500 characters as summary
    except Exception as e:
        return f"Error fetching URL: {str(e)}"

# Main function to get chatbot response
def get_response(user_id, user_input):

    # Load the model 
    if not os.path.exists(MODEL_FILE):
        raise FileNotFoundError("Chatbot model not found! Please run train_model.py first.")
    model = load_model(MODEL_FILE)

    if user_input.startswith('http://') or user_input.startswith('https://'):
        # If the input is a URL, fetch and summarize the content
        response = get_url_summary(user_input)
        log_chatbot_interaction(user_input, response)
        return response

    user_input_cleaned = user_input.lower().strip()

    # NLP prediction
    input_data = bow(user_input_cleaned, words)
    res = model.predict(np.array([input_data]))[0]

    results = [
        {'intent': classes[i], 'probability': str(r)}
        for i, r in enumerate(res) if r > 0.25
    ]
    results.sort(key=lambda x: x['probability'], reverse=True)

    if results:
        tag = results[0]['intent']
        for intent in intents['intents']:
            if intent['tag'] == tag:
                response = random.choice(intent['responses'])
                log_chatbot_interaction(user_input, response)
                return response
            
    for intent in intents['intents']:
        for pattern in intent.get('patterns', []):
            if pattern in user_input_cleaned:
                response = random.choice(intent['responses'])
                log_chatbot_interaction(user_input, response)
                return response

    response = "I'm sorry, I don't understand."
    log_chatbot_interaction(user_input, response)
    return response


# Create a Blueprint to separate chatbot routes
chatbot = Blueprint('chatbot', __name__)

@chatbot.route('/chat', methods=['POST', 'OPTIONS'])
def chat():
    if request.method == 'OPTIONS':
        return jsonify({'message': 'CORS preflight successful!'}), 200

    data = request.get_json()
    user_input = data.get('user_input', '').strip()
    
    if not user_input:
        return jsonify({'response': "Please enter a valid message."}), 400

    response = get_response(user_id=request.remote_addr, user_input=user_input)
    
    return jsonify({'response': response})

