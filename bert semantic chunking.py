import spacy
from transformers import BertTokenizer, BertModel
import torch
import numpy as np
from scipy.spatial.distance import pdist, squareform

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Load BERT tokenizer and model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained("bert-base-uncased")

def get_bert_embeddings(text):
    inputs = tokenizer(text, return_tensors="pt", max_length=512, truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        embeddings = outputs.last_hidden_state.squeeze().numpy()
    return embeddings


def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def semantic_chunking(text, threshold=0.7, max_length=512):
    # Split text into segments that fit within the max_length
    segments = [text[i:i+max_length] for i in range(0, len(text), max_length)]

    chunks = []
    for segment in segments:
        embeddings = get_bert_embeddings(segment)
        tokens = tokenizer.convert_ids_to_tokens(tokenizer(segment)['input_ids'])

        if embeddings.shape[0] == 0:
            continue

        similarities = squareform(pdist(embeddings, lambda u, v: cosine_similarity(u, v)))

        current_chunk = [tokens[0]]
        for i in range(1, len(tokens)):
            if i < similarities.shape[0] and similarities[i-1, i] > threshold:
                current_chunk.append(tokens[i])
            else:
                chunks.append(" ".join(current_chunk))
                current_chunk = [tokens[i]]

        if current_chunk:
            chunks.append(" ".join(current_chunk))

    return chunks


def query_chunks(chunks, keywords):
    # Find chunks containing all specified keywords
    relevant_chunks = []
    for chunk in chunks:
        if all(keyword.lower() in chunk.lower() for keyword in keywords):
            relevant_chunks.append(chunk)
    return relevant_chunks

# Example text
with open('event_default.txt', 'r', encoding="utf-8") as file:
    markdown_content = file.read()
# Perform semantic chunking
chunks = semantic_chunking(markdown_content, threshold=0.7)  # You can adjust the threshold

# Define keywords to query
keywords = ["Equity Cure"]

# Query chunks for keywords
relevant_chunks = query_chunks(chunks, keywords)

# Print relevant chunks
for i, chunk in enumerate(relevant_chunks):
    print(f"Relevant Chunk {i+1}: {chunk}")