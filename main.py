import smtplib
import ssl
import requests
import os
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration
email_sender = os.environ.get('email_sender')
email_receiver = os.environ.get('email_receiver')
# smtp_server = os.environ.get('smtp_server')
smtp_server = 'smtp.gmail.com'
port = 587  # For starttls



algae_password = os.environ.get('algae_password')


# Retrieve the API key from environment variables
api_key = os.environ.get('PERPLEXITY_API_KEY')


# Define the question to ask Perplexity AI

# Function to send email
def send_email(subject, body):
    message = MIMEMultipart()
    message["From"] = email_sender
    message["To"] = email_receiver
    message["Subject"] = subject

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.login(email_sender, algae_password)
        server.sendmail(email_sender, email_receiver, message.as_string())

# Function to get answer from Perplexity AI (mockup)
def get_answer_from_perplexity_ai():
    url = "https://api.perplexity.ai/chat/completions"

    payload = {
        "model": "llama-3.1-sonar-small-128k-online",
        "messages": [
            {
                "role": "system",
                "content": "Be precise and concise."
            },
            {
                "role": "user",
                "content": "Assume you are god of start-ups. Give me a small but effective idea to generate passive income by doing a website, or an app or an SaaS or an electronics related idea.Your answer should be detailed and should include all steps in order to realize the idea"
            }
        ],
        "max_tokens": 100,
        "temperature": 0.2,
        "top_p": 0.9,
        "return_citations": True,
        "search_domain_filter": ["perplexity.ai"],
        "return_images": False,
        "return_related_questions": False,
        "search_recency_filter": "month",
        "top_k": 0,
        "stream": False,
        "presence_penalty": 0,
        "frequency_penalty": 1
    }
    headers = {"Authorization": f"Bearer {api_key}" }

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.text)
    
    
    # Check if the request was successful
    if response.status_code == 200:
        # return response.json().get("message", "No answer received.")
        return response.text
    else:
        return f"Failed to get a response from Perplexity AI. Status Code: {response.status_code}"


def format_idea_for_email(json_response):
    # Parse the JSON response
    data = json.loads(json_response)
    
    # Extract relevant information
    choice = data['choices'][0]
    content = choice['message']['content']
    
    # Format as plain text or HTML
    formatted_content = f"""{content}"""
    return formatted_content



# Main function to execute daily task
def main():
    message = get_answer_from_perplexity_ai()
    formatted_content = format_idea_for_email(message)
    
    send_email("Daily Startup Idea", formatted_content)
    # send_email("Daily Startup Idea", message)

if __name__ == "__main__":
    main()