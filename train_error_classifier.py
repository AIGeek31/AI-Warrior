from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

# Example training data (replace with your real, private data)
texts = [
    "SyntaxError: invalid syntax in script",
    "Disk quota exceeded on server",
    "Product not found in inventory",
    "Unknown error occurred"
]
labels = [
    "script issue",
    "system issue",
    "product issue",
    "other"
]

# Train vectorizer and model
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)
model = LogisticRegression()
model.fit(X, labels)

# Save vectorizer and model
with open('my_vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)
with open('my_classifier.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Custom classifier and vectorizer saved as 'my_classifier.pkl' and 'my_vectorizer.pkl'.")
