import pandas as pd
import stanfordnlp
from spacy_stanfordnlp import StanfordNLPLanguage
from sklearn.feature_extraction.text import CountVectorizer

class Bag_Words(object):

    # config = None
    # nlp = None

    # def __init__(self):


    def __clean_text(self, df):
        config = {
            'processors': 'tokenize,pos,lemma,depparse',  # Comma-separated list of processors to use
            'lang': 'en',  # Language code for the language to build the Pipeline in
            'tokenize_model_path': 'C:\\Users\\79196\\stanfordnlp_resources\\ru_syntagrus_models\\ru_syntagrus_tokenizer.pt',
            'pos_model_path': 'C:\\Users\\79196\\stanfordnlp_resources\\ru_syntagrus_models\\ru_syntagrus_tagger.pt',
            'pos_pretrain_path': 'C:\\Users\\79196\\stanfordnlp_resources\\ru_syntagrus_models\\ru_syntagrus.pretrain.pt',
            'lemma_model_path': 'C:\\Users\\79196\\stanfordnlp_resources\\ru_syntagrus_models\\ru_syntagrus_lemmatizer.pt',
            'depparse_model_path': 'C:\\Users\\79196\\stanfordnlp_resources\\ru_syntagrus_models\\ru_syntagrus_parser.pt',
            'depparse_pretrain_path': 'C:\\Users\\79196\\stanfordnlp_resources\\ru_syntagrus_models\\ru_syntagrus.pretrain.pt'
        }

        snlp = stanfordnlp.Pipeline(**config)
        nlp = StanfordNLPLanguage(snlp)

        text_list = df["Text"].values
        lower_text_list = []
        for text in text_list:
            text_lower = text.lower()
            lower_text_list.append(text_lower)
        clean_text_list = []
        for text in lower_text_list:
            text = nlp(text)
            token = [token.orth_ for token in text if not token.is_punct]
            clean_text_list.append(token)
        return clean_text_list

    def bag_of_words(self, df):
        text = self.__clean_text(self, df)
        bag = None
        for phrase in text:
            print(phrase)
            vectorizer = CountVectorizer()
            bag = vectorizer.fit_transform(phrase).todense()
            print(bag)
        return bag

text_sentiment_columns = ['Text']
text = 'Биржа копирайтинга Text.ru — это достойный заработок для копирайтеров и возможность заказать текст у профессиональных авторов. Здесь вы можете реализовать свой творческий потенциал или приобрести уникальные статьи для нужд своего сайта.'
data = list()
data.append(text)
df = pd.DataFrame(data=data, columns = ['Text'])
b = Bag_Words.bag_of_words(Bag_Words, df)