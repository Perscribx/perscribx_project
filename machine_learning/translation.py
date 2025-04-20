from transformers import pipeline
import nltk

nltk.download("punkt")
from nltk.tokenize import sent_tokenize
languages = ['pol_Latn', 'spa_Latn', 'fra_Latn', 'deu_Latn', 'ita_Latn']

def split_into_chunks(text, max_chars=400):

    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_chars:
            current_chunk += " " + sentence
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def translate(text, source="eng_Latn", target="pol_Latn"):

    translator = pipeline("translation", model="facebook/nllb-200-distilled-600M", src_lang=source, tgt_lang=target,
                          max_length=512,truncation=True)

    chunks = split_into_chunks(text)
    translated = []

    for  chunk in chunks:
        result = translator(chunk)
        translated.append(result[0]['translation_text'])

    return "\n".join(translated)


if __name__ == "__main__":

    with open("summary.txt", "r", encoding="utf-8") as f:
        english_text = f.read()

    for language in languages:
        polish_translation = translate(english_text, target=language)

        with open(f"translations/{language}.txt", "w", encoding="utf-8") as f:
            f.write(polish_translation)

