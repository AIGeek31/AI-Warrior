import os
from typing import List
import smtplib
from email.mime.text import MIMEText
import pickle

# Define categories and their email aliases
CATEGORY_EMAILS = {
    'script issue': 'script-team@example.com',
    'system issue': 'sysadmin@example.com',
    'product issue': 'product-team@example.com',
    'other': 'support@example.com'
}

class ErrorClassifier:
    def __init__(self, categories: List[str]):
        self.categories = categories
        # Load your custom classifier and vectorizer
        with open('my_classifier.pkl', 'rb') as f:
            self.model = pickle.load(f)
        with open('my_vectorizer.pkl', 'rb') as f:
            self.vectorizer = pickle.load(f)

    def classify(self, error_message: str) -> str:
        X = self.vectorizer.transform([error_message])
        pred = self.model.predict(X)[0]
        # Optionally map model output to your categories
        return pred

def send_email(subject: str, body: str, to_email: str):
    # Configure your SMTP server here
    smtp_server = 'smtp.example.com'
    smtp_port = 587
    smtp_user = os.getenv('SMTP_USER')
    smtp_pass = os.getenv('SMTP_PASS')
    from_email = smtp_user

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(from_email, [to_email], msg.as_string())
    print(f"Email sent to {to_email}")

def process_error(error_message: str):
    categories = list(CATEGORY_EMAILS.keys())
    classifier = ErrorClassifier(categories)
    category = classifier.classify(error_message)
    #to_email = CATEGORY_EMAILS.get(category, CATEGORY_EMAILS['other'])
    subject = f"Error classified as: {category}"
    #send_email(subject, error_message, to_email)
    print(f"Error processed and reported as '{category}'")

# Example usage:
if __name__ == "__main__":
    error_msg = input("Paste the error message: ")
    process_error(error_msg)