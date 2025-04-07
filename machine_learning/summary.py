'''from transformers import BartTokenizer, BartForConditionalGeneration, pipeline

summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def summarize_text(text):
    return summarizer(text, max_length = 150, min_length = 30, do_sample=False)
    '''



