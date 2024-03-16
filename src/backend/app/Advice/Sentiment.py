import pandas as pd
from torch import nn
import torch
from transformers import DistilBertModel
from ..Recommendation.QueryBased import model_init, device
from ..Recommendation import QueryBased

sentiment = None


# 批量预测评论情感类别
def sentiment_predict(texts):
    global sentiment
    if QueryBased.tokenizer is None:
        # 初始化分词器
        model_init()
    if sentiment is None:
        # 初始化预训练语言模型
        bert_model = DistilBertModel.from_pretrained('config/model/distilbert-base-uncased')
        # 初始化情感分类模型
        sentiment = Sentiment(bert_model, 2)
        # 加载权重
        sentiment.load_state_dict(torch.load('config/model/sentiment.pt'))
        # 移动到CUDA
        sentiment.to(device)
    # 输入句子编码
    encoded_batch = QueryBased.tokenizer.batch_encode_plus(texts, add_special_tokens=True, return_tensors='pt',
                                                           padding=True, truncation=True, max_length=512).to(device)
    # 关闭梯度计算减小显存开销
    with torch.no_grad():
        # 进行预测
        predictions = sentiment(encoded_batch)
        probability = torch.softmax(predictions, dim=1)
        predicted_class = predictions.argmax(dim=1)
        predicted_probability = torch.max(probability, dim=1).values
        predicted_class = predicted_class
        # 根据预测置信度确定中性情感
        predicted_class[predicted_probability < 0.6] = 2
    # 返回结果dataframe
    result_df = pd.DataFrame({
        'text': texts,
        'sentiment': predicted_class.cpu().numpy(),
        'predicted_probability': predicted_probability.cpu().numpy()
    })
    return result_df


# 情感分析模型
class Sentiment(nn.Module):
    def __init__(self, bert_model, output_dim):
        super().__init__()
        # 文本编码bert
        self.transformer = bert_model
        # 分类头
        self.fc = nn.Linear(768, output_dim)

    def forward(self, encoded_batch):
        # 前馈过程
        output = self.transformer(**encoded_batch)
        hidden = output.last_hidden_state
        cls_hidden = hidden[:, 0, :]
        prediction = self.fc(torch.tanh(cls_hidden))
        return prediction


def analyze_reviews_for_business(reviews_df):
    # 获取当前business_id下的所有评论文本
    review_texts = reviews_df['rev_text'].tolist()
    # 调用sentiment_predict函数进行情感分析
    result_df = sentiment_predict(review_texts)
    # 统计正面、负面、中性评论数量
    positive_reviews_count = len(result_df[result_df['sentiment'] == 1])
    negative_reviews_count = len(result_df[result_df['sentiment'] == 0])
    normal_reviews_count = len(result_df[result_df['sentiment'] == 2])
    return positive_reviews_count, negative_reviews_count, normal_reviews_count

# def sentiment_predict(texts):
#     global sentiment
#     if QueryBased.model is None or QueryBased.tokenizer is None:
#         model_init()
#     if sentiment is None:
#         sentiment = Sentiment(QueryBased.model, 2)
#         sentiment.cls_head.load_state_dict(torch.load("config/model/sentiment.pt"))
#         sentiment.cls_head.to(device)
#
#     encoded_batch = QueryBased.tokenizer.batch_encode_plus(texts, add_special_tokens=True, return_tensors='pt', padding=True, truncation=True).to(device)
#     with torch.no_grad():
#         predictions = sentiment(encoded_batch)
#         probability = torch.softmax(predictions, dim=1)
#         predicted_class = predictions.argmax(dim=1)
#         predicted_probability = torch.max(probability , dim=1).values
#     print(predicted_class)
#     print(predicted_probability)
#     return predicted_class, predicted_probability
#
#
# class Sentiment(nn.Module):
#     def __init__(self, bert_model, output_dim):
#         super().__init__()
#         self.bert_model = bert_model
#         self.cls_head = nn.Linear(768, output_dim)
#         for param in self.bert_model.parameters():
#             param.requires_grad = False
#         for param in self.cls_head.parameters():
#             param.requires_grad = False
#
#     def forward(self, encoded_batch):
#         #  encoded_batch = [batch size, seq len]
#         cls_hidden = self.bert_model(**encoded_batch).last_hidden_state.mean(dim=1)
#         prediction = self.cls_head(torch.tanh(cls_hidden))
#         # prediction = [batch size, output dim]
#         return prediction
