
from transformers import pipeline, AutoModelForSeq2SeqLM, MBartForConditionalGeneration, MBart50TokenizerFast

summariser = pipeline("summarization", model="facebook/bart-large-cnn")
model_name = "Helsinki-NLP/opus-mt-en-mul"

model = MBartForConditionalGeneration.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")
tokenizer = MBart50TokenizerFast.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")

def split_text(text):

    amount_of_blocks = ( len(text) // 500 ) + 1
    blocks = []

    for x in range(amount_of_blocks):

      blocks.append([text[x * 500 : 500 * (x + 1)]])

    return blocks

def translation_to_eng(text):

    translator_pl_en = pipeline("translation", model="Helsinki-NLP/opus-mt-pl-en")
    eng_text = translator_pl_en(text)[0]['translation_text']

    return eng_text

def translation_to_pl(text):
    tokenizer.src_lang = "en_XX"
    encoded_pl = tokenizer(text, return_tensors='pt')
    tokens = model.generate(
        **encoded_pl, forced_bos_token_id=tokenizer.lang_code_to_id["pl_PL"]
    )

    return tokenizer.batch_decode(tokens, skip_special_tokens=True)



def summarise(text):
    summaries = []
    text_in_blocks = split_text(text)
    translated_blocks = [translation_to_eng(block) for block in text_in_blocks]
    summarised_text = summariser(translated_blocks, max_length=20, min_length=5, do_sample=False, batch_size=6)
    summaries.extend([s['summary_text'] for s in summarised_text])
    string = ""
    summaries = [translation_to_pl(s) for s in summaries]
    for x in summaries:
        string += " ".join(x)  # Join the list into a single string and then concatenate

    return string


