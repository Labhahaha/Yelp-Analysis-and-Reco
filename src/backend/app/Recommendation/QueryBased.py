import pandas as pd
from transformers import DistilBertTokenizer, DistilBertModel
import torch

tokenizer = None
model = None

def model_init():
    global model,tokenizer
    tokenizer = DistilBertTokenizer.from_pretrained('config/model/distilbert-base-uncased')
    model = DistilBertModel.from_pretrained('config/model/distilbert-base-uncased')

def encode_texts(texts):
    # texts 是一个包含搜索查询和商业文本的列表
    encoded_batch = tokenizer.batch_encode_plus(texts, add_special_tokens=True, return_tensors='pt', padding=True, truncation=True)
    with torch.no_grad():
        vectors = model(**encoded_batch).last_hidden_state.mean(dim=1)
        query_vec = vectors[0].unsqueeze(0)
        business_vecs = vectors[1:]
    return query_vec, business_vecs

def cosine_similarity(a, b):
    return torch.nn.functional.cosine_similarity(a, b, dim=-1)

def match_rating(search_query, business_texts):
    if model is None or tokenizer is None:
        model_init()
    texts = [search_query] + business_texts['business_text'].tolist()
    query_vec, business_vecs = encode_texts(texts)
    similarities = cosine_similarity(query_vec, business_vecs)
    rating_df = pd.DataFrame(similarities.cpu().numpy(), columns=['match_rating'])
    return rating_df
