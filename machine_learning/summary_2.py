from transformers import MarianMTModel, MarianTokenizer, pipeline
import torch
import nltk

# Download NLTK sentence tokenizer
nltk.download('punkt')
from nltk.tokenize import sent_tokenize


model_name = "Helsinki-NLP/opus-mt-pl-en"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=0 if torch.cuda.is_available() else -1)

def split_text_to_chunks(text, max_tokens=512):

    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = []
    current_len = 0

    for sentence in sentences:
        sentence_tokens = tokenizer.tokenize(sentence)
        if current_len + len(sentence_tokens) <= max_tokens:
            current_chunk.append(sentence)
            current_len += len(sentence_tokens)
        else:
            if current_chunk:
                chunks.append(" ".join(current_chunk))
            current_chunk = [sentence]
            current_len = len(sentence_tokens)

    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks

def translate_polish_text(long_text):
    translated_text = []
    chunks = split_text_to_chunks(long_text)

    for  chunk in chunks:
        inputs = tokenizer(chunk, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            outputs = model.generate(**inputs)
        english_sentences = tokenizer.batch_decode(outputs, skip_special_tokens=True)
        translated_text.extend(english_sentences)

    return "\n".join(translated_text)


def text_split_for_summary(text, max_chars=3000):
    paragraphs = text.split("\n")
    current_chunk = ""
    chunks = []

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        if len(current_chunk) + len(para) < max_chars:
            current_chunk += " " + para
        else:
            chunks.append(current_chunk.strip())
            current_chunk = para
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks


def summarize_text(english_text):
    chunks = text_split_for_summary(english_text)
    summaries = summarizer(chunks, max_length=300, min_length=80, do_sample=False)
    return "\n\n".join([s['summary_text'] for s in summaries])


if __name__ == "__main__":
    with open("test.txt", "r", encoding="utf-8") as f:
        polish_text = f.read()

    english_translation = translate_polish_text(polish_text)

    with open("translated_to_english.txt", "w", encoding="utf-8") as f:
        f.write(english_translation)

    summary = summarize_text(english_translation)

    with open("summary.txt", "w", encoding="utf-8") as f:
        f.write(summary)

