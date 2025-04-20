from gtts import gTTS
import os


languages = ['en', 'pl', 'de', 'it', 'es', 'fr']
current_directory = os.getcwd()
current_directory =  os.path.join(current_directory, 'translations')
files = [f for f in os.listdir(current_directory) if os.path.isfile(os.path.join(current_directory, f))]
print(files)

def make_voice_over(language, text):
    recording = gTTS(text=text, lang=language, slow=False)
    recording.save(f"voice_overs/{language}.mp3")

for language in languages:

    for file in files:
        if language in file or ('pol' in file and language == 'pl') or ('spa' in file and language == 'es'):

            with open(f'translations/{file}', "r", encoding="utf-8") as f:
                text = f.read()

            make_voice_over(language, text)





