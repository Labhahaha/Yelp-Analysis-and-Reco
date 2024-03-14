import pandas as pd
from torch import nn
import torch
from transformers import DistilBertModel
from ..Recommendation.QueryBased import model_init, device
from ..Recommendation import QueryBased

sentiment = None

def sentiment_predict(texts):
    global sentiment
    if QueryBased.tokenizer is None:
        model_init()
    if sentiment is None:
        bert_model = DistilBertModel.from_pretrained('config/model/distilbert-base-uncased')
        sentiment = Sentiment(bert_model, 2)
        sentiment.load_state_dict(torch.load('config/model/sentiment.pt'))
        sentiment.to(device)

    encoded_batch = QueryBased.tokenizer.batch_encode_plus(texts, add_special_tokens=True, return_tensors='pt', padding=True).to(device)
    with torch.no_grad():
        predictions = sentiment(encoded_batch)
        probability = torch.softmax(predictions, dim=1)
        predicted_class = predictions.argmax(dim=1)
        predicted_probability = torch.max(probability , dim=1).values
        predicted_class = predicted_class
        predicted_class[predicted_probability<0.6] = 2

    result_df = pd.DataFrame({
        'text': texts,
        'predicted_class': predicted_class.cpu().numpy(),
        'predicted_probability': predicted_probability.cpu().numpy()
    })
    return result_df


class Sentiment(nn.Module):
    def __init__(self, bert_model, output_dim):
        super().__init__()
        self.transformer = bert_model
        self.fc = nn.Linear(768, output_dim)
    def forward(self, encoded_batch):
        output = self.transformer(**encoded_batch)
        hidden = output.last_hidden_state
        cls_hidden = hidden[:, 0, :]
        prediction = self.fc(torch.tanh(cls_hidden))
        return prediction

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

