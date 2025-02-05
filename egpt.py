from flask import Flask, render_template_string, request
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import random

# Download necessary resources (only needed once)
nltk.download('vader_lexicon')

# Initialize Flask app
app = Flask(__name__)

# Initialize Sentiment Analyzer
sia = SentimentIntensityAnalyzer()

# Predefined responses based on sentiment
RESPONSES = {
    "positive": [
        "I'm glad to hear that! 😊 Keep spreading positivity!",
        "That sounds amazing! What made your day so great?",
        "Happiness looks good on you! Tell me more!"
    ],
    "neutral": [
        "I see! Would you like to share more?",
        "Got it! What else is on your mind?",
        "That makes sense. What's next for you?"
    ],
    "negative": [
        "I'm here for you. Want to talk about it?",
        "That sounds tough. Remember, you're not alone. 💙",
        "I'm listening. Feel free to share your thoughts."
    ],
    "unknown": [
        "I'm not sure I understand, but I'm here to listen!",
        "Could you rephrase that? I want to respond better.",
        "That's interesting! Can you tell me more?"
    ]
}

def get_sentiment(text):
    """Analyze sentiment of the input text."""
    scores = sia.polarity_scores(text)
    if scores['compound'] >= 0.3:
        return "positive"
    elif scores['compound'] <= -0.3:
        return "negative"
    else:
        return "neutral"

def get_response(user_input):
    """Get chatbot response based on sentiment."""
    sentiment = get_sentiment(user_input)
    return random.choice(RESPONSES.get(sentiment, RESPONSES["unknown"]))

# HTML and JavaScript for Chatbot UI
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Echo of Empathy</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            background-color: #f0f2f5;
        }
        #chatbox {
            width: 60%;
            margin: auto;
            background: white;
            padding: 20px;
            box-shadow: 0px 0px 10px gray;
            border-radius: 10px;
        }
        .message {
            text-align: left;
            padding: 10px;
        }
        .user {
            color: blue;
            font-weight: bold;
        }
        .bot {
            color: green;
            font-weight: bold;
        }
        input[type="text"] {
            width: 80%;
            padding: 10px;
            margin-top: 10px;
        }
        button {
            padding: 10px;
            background-color: blue;
            color: white;
            border: none;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <h1>Echo of Empathy 🤖</h1>
    <div id="chatbox">
        <div id="chat"></div>
        <input type="text" id="user_input" placeholder="Type a message...">
        <button onclick="sendMessage()">Send</button>
    </div>

    <script>
        function sendMessage() {
            let userMessage = document.getElementById("user_input").value;
            let chat = document.getElementById("chat");

            if (userMessage.trim() === "") return;

            // Display user message
            chat.innerHTML += `<p class='user message'>You: ${userMessage}</p>`;

            // Send message to server
            fetch("/get_response", {
                method: "POST",
                body: new URLSearchParams({ user_message: userMessage }),
                headers: { "Content-Type": "application/x-www-form-urlencoded" }
            })
            .then(response => response.text())
            .then(botReply => {
                chat.innerHTML += `<p class='bot message'>Chatbot: ${botReply}</p>`;
            });

            // Clear input field
            document.getElementById("user_input").value = "";
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/get_response", methods=["POST"])
def chatbot_response():
    user_message = request.form["user_message"]
    bot_reply = get_response(user_message)
    return bot_reply

if __name__ == "__main__":
    app.run(debug=True)
