from sklearn.linear_model import LogisticRegression
import pickle
from transformers import BertTokenizer, BertModel
import torch

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

# Load pre-trained BERT tokenizer and model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
bert_model = BertModel.from_pretrained('bert-base-uncased')

def get_bert_embeddings(texts):
    inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        outputs = bert_model(**inputs)
    # Use the [CLS] token embedding as the sentence embedding
    embeddings = outputs.last_hidden_state[:, 0, :].numpy()
    return embeddings

X = get_bert_embeddings(texts)
model = LogisticRegression(max_iter=1000)
model.fit(X, labels)

# Save vectorizer and model
with open('my_classifier.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Custom classifier saved as 'my_classifier.pkl'.")
