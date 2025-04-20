from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk import word_tokenize
import string



#for tokenization
#nltk.download('punkt_tab')

#for lemmanization
#nltk.download('wordnet')

#downloading stopwords
#nltk.download('stopwords')
stopwords_list = set(stopwords.words('english'))


def processing_text_data(data, tokenization=True, lemmanization=True, stopwords=True, lowercasing=True, punctuation=True):
    '''
    Processing text data
    :param data: the data we want to process
    :param tokenization: whether we want to tokenize the data
    :param lemmanization: boiling down the word to its root
    :param stopwords: words that are not that important
    :param lowercasing: changing the size of the letter
    :param punctuation: the choice whether the punctuation is needed
    :return: processed data
    '''

    tokenized_data = []

    for row in data:

        tokenized_row =  str(row)
        if tokenization:
            tokenized_row = word_tokenize(tokenized_row)
        if punctuation:
            tokenized_row = [word for word in tokenized_row if word not in string.punctuation]
        if lowercasing:
            tokenized_row = [str.lower(word) for word in tokenized_row]
        if stopwords:
            tokenized_row = [word for word in tokenized_row if word not in stopwords_list]
        if lemmanization:
            lem = WordNetLemmatizer()
            tokenized_row = [lem.lemmatize(word) for word in tokenized_row]

        tokenized_data.append(tokenized_row)

    return tokenized_data
