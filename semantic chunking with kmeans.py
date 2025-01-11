import spacy
from transformers import BertTokenizer, BertModel
import torch
import numpy as np
from sklearn.cluster import KMeans

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Load BERT tokenizer and model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained("bert-base-uncased")

def get_bert_embeddings(text_segment):
    inputs = tokenizer(text_segment, return_tensors="pt", max_length=512, truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        embeddings = outputs.last_hidden_state.squeeze().numpy()
    return embeddings

def semantic_chunking(text, num_chunks=5, max_length=512):
    # Split text into segments that fit within the max_length
    segments = [text[i:i+max_length] for i in range(0, len(text), max_length)]

    all_chunks = []
    for segment in segments:
        embeddings = get_bert_embeddings(segment)
        tokens = tokenizer.convert_ids_to_tokens(tokenizer(segment)['input_ids'])

        if embeddings.shape[0] == 0:
            continue

        # Perform k-means clustering
        kmeans = KMeans(n_clusters=num_chunks, random_state=0).fit(embeddings)
        labels = kmeans.labels_

        # Create chunks based on cluster labels
        chunks = [""] * num_chunks
        for token, label in zip(tokens, labels):
            chunks[label] += token + " "

        # Remove trailing spaces and filter out empty chunks
        chunks = [chunk.strip() for chunk in chunks if chunk.strip()]

        all_chunks.extend(chunks)

    return all_chunks

def query_chunks(chunks, keywords):
    relevant_chunks = []
    for chunk in chunks:
        if all(keyword.lower() in chunk.lower() for keyword in keywords):
            relevant_chunks.append(chunk)
    return relevant_chunks

# Example text
# Example text
with open('event_default.txt', 'r', encoding="utf-8") as file:
    markdown_content = file.read()
# Perform semantic chunking
chunks = semantic_chunking(markdown_content, num_chunks=3)  # You can adjust the number of chunks

# Define keywords to query
keywords = ["Equity Cure"]

# Query chunks for keywords
relevant_chunks = query_chunks(chunks, keywords)

# Print relevant chunks
for i, chunk in enumerate(relevant_chunks):
    print(f"Relevant Chunk {i+1}: {chunk}")
