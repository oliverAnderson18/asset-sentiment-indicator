from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import pandas as pd

model_name = "yiyanghkust/finbert-tone"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

labels = ["Positive", "Neutral", "Negative"]
labels_score = {"Positive": 1, "Neutral": 0, "Negative": -1}

def sentiment_score(row: pd.Series) -> float:
    texts = [row["title"], row["description"], row["content"]]
    
    scores = []
    for text in texts:
        text = str(text) if pd.notna(text) else ""
        if text.strip() == "":
            continue
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        pred_label = labels[torch.argmax(probs)]
        scores.append(labels_score[pred_label])
    
    avg_score = sum(scores) / len(scores) if scores else 0
    percent = (avg_score + 1) * 50
    return percent

