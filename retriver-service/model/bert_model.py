import pandas as pd
import numpy as np
import torch
from sklearn.metrics.pairwise import cosine_similarity
from model import model, tokenizer, df, data_vectors

__max_similarity_documents__ = 3

#Mean Pooling - Take attention mask into account for correct averaging
def __mean_pooling__(model_output, attention_mask):
    token_embeddings = model_output[0] #First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
    sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    return sum_embeddings / sum_mask

def __get_text_vector__(sentences):
    encoded_input = tokenizer(sentences, padding=True, truncation=True, max_length=100, return_tensors='pt')

    with torch.no_grad():
        model_output = model(**encoded_input)

    return __mean_pooling__(model_output, encoded_input['attention_mask'])

def __prepare_requet__(request):
    return np.nan_to_num(np.array(__get_text_vector__(request)))

def find_similarity_documents(request) -> []:
    results = []

    cosine_similarities = pd.Series(cosine_similarity(__prepare_requet__(request), data_vectors).flatten())

    for i,j in cosine_similarities.nlargest(__max_similarity_documents__).items():
        results.append({'weight':str(j), 'entity_chiper':df.title.iloc[i], 'raw_text':df.text.iloc[i]})

    return results;