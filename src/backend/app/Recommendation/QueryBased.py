import pandas as pd
from transformers import DistilBertTokenizer, DistilBertModel
import torch

tokenizer = DistilBertTokenizer.from_pretrained('config/model/distilbert-base-uncased')
model = DistilBertModel.from_pretrained('config/model/distilbert-base-uncased')

def encode_business_info(business_texts):
    encoded_info = tokenizer.batch_encode_plus(business_texts, add_special_tokens=True, return_tensors='pt',
                                               padding=True, truncation=True)
    with torch.no_grad():
        business_vecs = model(**encoded_info).last_hidden_state.mean(dim=1)
    return business_vecs

def encode_search_query(search_query):
    encoded_query = tokenizer.encode_plus(search_query, add_special_tokens=True, return_tensors='pt', padding=True,
                                          truncation=True)
    with torch.no_grad():
        query_vec = model(**encoded_query).last_hidden_state.mean(dim=1)
    return query_vec

def cosine_similarity(a, b):
    return torch.nn.functional.cosine_similarity(a, b, dim=-1)

def match_rating(search_query, business_texts):
    business_texts = business_texts['business_text'].tolist()
    query_vec = encode_search_query(search_query)
    business_vecs = encode_business_info(business_texts)
    similarities = cosine_similarity(query_vec, business_vecs)
    rating_df = pd.DataFrame(similarities.cpu().numpy(), columns=['match_rating'])
    return rating_df