import spacy
from transformers import BertTokenizer, BertModel
import torch

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Load BERT tokenizer and model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained("bert-base-uncased")
def semantic_chunking(text):
    # Process text with spaCy
    doc = nlp(text)

    # Tokenize text for BERT
    inputs = tokenizer(text, return_tensors="pt", max_length=512, truncation=True, padding=True)

    # Get BERT embeddings
    with torch.no_grad():
        outputs = model(**inputs)
        embeddings = outputs.last_hidden_state

    # Convert embeddings to numpy array
    embeddings = embeddings.squeeze().numpy()

    # Initialize chunk list
    chunks = []

    # Iterate over spaCy tokens
    current_chunk = []
    for token in doc:
        token_text = token.text

        # Simple heuristic for chunking: start a new chunk after a punctuation mark
        if token.is_punct:
            if current_chunk:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
        else:
            current_chunk.append(token_text)

    # Add the last chunk if any
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
chunks = semantic_chunking(markdown_content)

# Define keywords to query
keywords = ["Equity Cure"]

# Query chunks for keywords
relevant_chunks = query_chunks(chunks, keywords)

# Print relevant chunks
for i, chunk in enumerate(relevant_chunks):
    print(f"Relevant Chunk {i+1}: {chunk}")
