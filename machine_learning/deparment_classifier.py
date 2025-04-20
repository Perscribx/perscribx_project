from sklearn.metrics.pairwise import cosine_similarity

import json
from preprocess_text import processing_text_data
import pandas as pd
from transformers import AutoTokenizer, AutoModel
import torch
from scipy.spatial.distance import cosine

with open('department.json', 'r') as d:
    departments = json.load(d)

df = pd.DataFrame(departments)

with open('test.txt', 'r',  encoding="utf-8") as f:
    text = f.read()

model_name = "allegro/herbert-base-cased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

def get_word_embedding(word):
    inputs = tokenizer(word, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)

    embeddings = outputs.last_hidden_state
    return embeddings[0, 0, :].numpy()

word1 = "wiedza"
word2 = "inteligencja"

embedding1 = get_word_embedding(word1)
embedding2 = get_word_embedding(word2)

similarity = 1 - cosine(embedding1, embedding2)
print(f"Cosine similarity between '{word1}' and '{word2}': {similarity:.4f}")

text = text.split()
processed_text = processing_text_data(text)
departments_names = df.columns

correct_dep = []

for word in text:

    max_similarity_word = 0

    for department in departments_names:

        for word_2 in departments[department]:
            embedding1 = get_word_embedding(word)
            embedding2 = get_word_embedding(word_2)
            similarity = 1 - cosine(embedding1, embedding2)

            if similarity > 0.99:
                correct_dep.append(department)






