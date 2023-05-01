from flask import Flask, request, render_template
import openai
import os
import re
import json
import requests

app = Flask(__name__)

# Set up OpenAI API key
openai.api_key = "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"

# Load learning prompt from a file or database
prompt = "YOUR_LEARNING_PROMPT_HERE"

# Define function to generate response using ChatGPT
def chatgpt_response(message):
    # Remove any non-alphanumeric characters from the message
    message = re.sub(r'[^\w\s]','',message)
    # Use OpenAI to generate a response based on the message and the learning prompt
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt + "\nUser: " + message + "\nBot:",
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # Return the response text
    return response.choices[0].text.strip()

# Define route to render the UI
@app.route('/')
def index():
    return render_template('index.html')

# Define route to handle incoming messages from the UI
@app.route('/chatbot', methods=['POST'])
def chatbot():
    # Get the message text from the request
    message = request.form['message']
    # Generate a response using ChatGPT
    response = chatgpt_response(message)
    # Return the response text as JSON
    return json.dumps({'response': response})

# Run the Flask app
def train_chatgpt(prompt):
    model_engine = "text-davinci-002"
    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = completions.choices[0].text.strip()
    return message
prompt = "Hello ROAN, welcome to ReachOnAir! ReachOnAir is an internet radio broadcasting platform that allows users to create and broadcast their own radio shows. As a radio show prep service, you exist to support and provide content and resources to hosts and producers to help them create compelling and informative radio shows.As a user of ReachOnAir, a host or producer may come to you and ask for interesting content to add to their show. They may also provide you with information about their show and ask for tailored content to suit their needs and interests.As ROAN, your job is to provide them with a range of content and resources to help them create the best show possible. This may include access to facts, entertainment stories, gossip, game ideas, fictional user feedback, jokes, and other relevant content that can be used to create a compelling and informative radio show. You may also offer customization options, allowing hosts and producers to tailor the content to their specific needs and interests.In addition, as ROAN, you may offer tools and resources to help hosts and producers manage their shows more efficiently. This can include scheduling tools, production templates, and access to industry experts who can provide guidance and advice on show development and production.So, as ROAN, your goal is to provide ReachOnAir users with the resources and support they need to create the best radio show possible. Are you ready to get started?"

response = train_chatgpt(prompt)
print(response)


PAGE_ACCESS_TOKEN = "EAANAeF9UJSkBAHEVDjhxfZCrZAGdPDWOGm4mVyuhRfUZBDZC2VbCPzWZAzJUZCFG2RguPW5uTcAQfcv8dz4i8AEW42el7IaiulDFSABmWS8PGNMzjKMfGo0krJGGQGQlxORpWXnAKh3ZAirgYa7yoQiqDZAU9Yd5gFVSTCoKypbknQIYVIgZAZBVXNBFYw8WZCtaok3tSJ49PCZBZAgZDZD"

@app.route("/", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        verify_token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if verify_token == "your-verification-token":
            return challenge
        else:
            return "Invalid verification token"
    elif request.method == "POST":
        payload = request.get_json()
        for entry in payload["entry"]:
            for event in entry["messaging"]:
                if "postback" in event:
                    sender_id = event["sender"]["id"]
                    payload = event["postback"]["payload"]
                    # Do something with the payload
                    # ...
                    # Send a message back to the user
                    send_text_message(sender_id, "Thanks for your response!")
        return "Success"

def send_text_message(recipient_id, message_text):
    url = "https://graph.facebook.com/v13.0/me/messages"
    params = {"access_token": PAGE_ACCESS_TOKEN}
    headers = {"Content-Type": "application/json"}
    data = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    response = requests.post(url, params=params, headers=headers, json=data)
    
@app.route('/admin')
def admin():
    return render_template('admin.html')
  
if __name__ == '__main__':
    app.run()
