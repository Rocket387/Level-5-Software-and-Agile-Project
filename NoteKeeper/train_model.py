import nltk
import json
import pickle
import numpy as np
import random
import os
import ssl
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD

# Disable SSL verification (for nltk downloads)
ssl._create_default_https_context = ssl._create_unverified_context

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

lemmatizer = WordNetLemmatizer()

# Load intents.json
# Load intents.json
with open(os.path.join(os.path.dirname(__file__), 'intents.json'), 'r') as file:
    intents = json.load(file)


words, classes, documents = [], [], []
ignore_words = ['?', '!']

for intent in intents['intents']:
    for pattern in intent['patterns']:
        w = nltk.word_tokenize(pattern.lower())
        words.extend(w)
        documents.append((w, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = sorted(set([lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]))
classes = sorted(set(classes))

# Save data
MODEL_DIR = os.path.dirname(__file__)
pickle.dump(words, open(os.path.join(MODEL_DIR, 'words.pkl'), 'wb'))
pickle.dump(classes, open(os.path.join(MODEL_DIR, 'classes.pkl'), 'wb'))


# Prepare training data
training, output_empty = [], [0] * len(classes)

for doc in documents:
    bag = [1 if w in [lemmatizer.lemmatize(word.lower()) for word in doc[0]] else 0 for w in words]
    output_row = output_empty[:]
    output_row[classes.index(doc[1])] = 1
    training.append([bag, output_row])

random.shuffle(training)
training = np.array(training, dtype=object)

train_x = np.array(list(training[:, 0]), dtype=np.float32)
train_y = np.array(list(training[:, 1]), dtype=np.float32)

# Train and save model
MODEL_FILE = os.path.join(MODEL_DIR, 'chatbot_model.h5')
if not os.path.exists(MODEL_FILE):
    model = Sequential([
        Dense(128, input_shape=(len(train_x[0]),), activation='relu'),
        Dropout(0.5),
        Dense(64, activation='relu'),
        Dropout(0.5),
        Dense(len(train_y[0]), activation='softmax')
    ])
    sgd = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
    model.fit(train_x, train_y, epochs=200, batch_size=5, verbose=1)
    model.save(MODEL_FILE)
    print("Model trained and saved as chatbot_model.h5.")
else:
    print("Model already exists. Delete chatbot_model.h5 to retrain.")