import pandas as pd
import torch
from transformers import DistilBertTokenizer, DistilBertModel

'''
使用语言模型bert，实现文本语义相似度匹配，使用搜索功能
'''
# 初始化分词器，模型和运行设备
tokenizer = None
model = None
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


# 初始化模型加载预训练权重
def model_init():
    global model, tokenizer
    tokenizer = DistilBertTokenizer.from_pretrained('config/model/distilbert-base-uncased')
    model = DistilBertModel.from_pretrained('config/model/distilbert-base-uncased')
    model.to(device)


# 编码文本获得文本语义嵌入
def encode_texts(texts):
    # 编码文本列表
    encoded_batch = tokenizer.batch_encode_plus(texts, add_special_tokens=True, return_tensors='pt', padding=True,
                                                truncation=True, max_length=512).to(device)
    # 关闭梯度计算节省资源与时间
    with torch.no_grad():
        vectors = model(**encoded_batch).last_hidden_state.mean(dim=1)
        query_vec = vectors[0].unsqueeze(0)
        business_vecs = vectors[1:]
    return query_vec, business_vecs


# 计算查询与商家信息prompt间的余弦相似度
def cosine_similarity(a, b):
    return torch.nn.functional.cosine_similarity(a, b, dim=-1)


# 计算查询与商家信息prompt间的匹配程度，进行基于搜索的推荐
def match_rating(search_query, business_texts):
    # 若模型未初始化则初始化模型
    if model is None or tokenizer is None:
        model_init()
    # 初始化待编码文本列表
    texts = [search_query] + business_texts['business_text'].tolist()
    # 编码得到特征嵌入
    query_vec, business_vecs = encode_texts(texts)
    # 计算语义相似度(匹配程度)
    similarities = cosine_similarity(query_vec, business_vecs)
    # 返回商家推荐列表
    rating_df = pd.DataFrame(similarities.cpu().numpy(), columns=['match_rating'])
    return rating_df
