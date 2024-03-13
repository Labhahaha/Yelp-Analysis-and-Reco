# from flask import request, jsonify
from transformers import DistilBertTokenizer, DistilBertModel
import numpy as np
import torch
seed = 1234

np.random.seed(seed)
torch.manual_seed(seed)
torch.cuda.manual_seed(seed)
torch.backends.cudnn.deterministic = True
# from ..Recommendation.Recommend import business_df, review_df

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def starsCount():
    pass

def sentimentAnalysis():
    tokenizer = DistilBertTokenizer.from_pretrained('../../config/model/distilbert-base-uncased')
    model = DistilBertModel.from_pretrained('../../config/model/distilbert-base-uncased')
    model = model.to(device)
    model.load_state_dict(torch.load("../../config/model/distilbert-base-uncased/transformer.pt"))

    text = "This film is great!"

    predicted_class, predicted_probability=predict_sentiment(text, model, tokenizer, device)
    print(predicted_class, predicted_probability)
    return


def predict_sentiment(text, model, tokenizer, device):
    ids = tokenizer(text)["input_ids"]
    tensor = torch.LongTensor(ids).unsqueeze(dim=0).to(device)
    prediction = model(tensor).squeeze(dim=0)
    probability = torch.softmax(prediction, dim=-1)
    predicted_class = prediction.argmax(dim=-1).item()
    predicted_probability = probability[predicted_class].item()
    return predicted_class, predicted_probability

sentimentAnalysis()