import pandas as pd
import torch
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity

# Load pre-trained BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')


def get_bert_embedding(text):
    """
    Generates BERT embeddings for a given text.

    Args:
        text (str): The input text.

    Returns:
        torch.Tensor: The BERT embedding.
    """
    inputs = tokenizer(text, return_tensors='pt', truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1)


def extract_most_similar_sentences(text, question):
    """
    Extracts the most similar sentences from a text based on a question using BERT embeddings.

    Args:
        text (str): The text of the loan agreement.
        question (str): The question to be answered.

    Returns:
        list: A list of the most similar sentences.
    """
    question_embedding = get_bert_embedding(question)

    # Split the text into sentences
    sentences = [sentence.strip() for sentence in text.split("\n\n") if sentence.strip()]
    if not sentences:
        return []

    sentence_embeddings = [get_bert_embedding(sentence) for sentence in sentences]

    # Calculate cosine similarity between question and each sentence
    similarities = [cosine_similarity(question_embedding, sentence_embedding)[0][0] for sentence_embedding in
                    sentence_embeddings]

    # Get the indices of the top 3 most similar sentences
    num_sentences = min(3, len(sentences))
    most_similar_indices = sorted(range(len(similarities)), key=lambda i: similarities[i], reverse=True)[:num_sentences]

    # Return the most similar sentences
    most_similar_sentences = [sentences[i] for i in most_similar_indices]
    most_similar_sentences_text = "\n\n".join(most_similar_sentences)
    return most_similar_sentences_text


def process_loan_agreements(csv_file, question):
    """
    Processes a CSV file containing loan agreement data to extract the most similar sentences using BERT.

    Args:
        csv_file (str): The path to the CSV file.
        question (str): The question to be answered.

    Returns:
        pandas.DataFrame: A DataFrame with the extracted most similar sentences.
    """
    df = pd.read_csv(csv_file)
    df['most_similar_sentences'] = None

    for index, row in df.iterrows():
        # if row['term_value'] == True:
        text = row['term_source']
        most_similar_sentences = extract_most_similar_sentences(text, question)
        df.loc[index, 'most_similar_sentences'] = most_similar_sentences

    return df


# Example usage:
csv_file = 'adj_ebidta_csv.csv'
question = "is there any exceptional item add back?"
# question = "What is the number of cures?"
df_results = process_loan_agreements(csv_file, question)
print(df_results[['document_name', 'most_similar_sentences']])