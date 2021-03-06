import pandas as pd
import numpy as np
import stanfordnlp
from spacy_stanfordnlp import StanfordNLPLanguage
from sklearn.feature_extraction.text import CountVectorizer

#Что нужно, чтобы установить нлп стэнфорд библиотеку
# use new conda env 3.7.
# Open conda terminal
# add command: conda install pytorch=0.4.1 -c pytorch
# after pip install stanfordnlp
# pip install spacy-stanfordnlp

class Bag_Words(object):
    #текст к нижнему регистру, убирает пунктуацию, стоп-слова, лемматизирует
    def __clean_text(self, df):
        config = {
            'processors': 'tokenize,pos,lemma,depparse',  # Comma-separated list of processors to use
            'lang': 'ru',  # Language code for the language to build the Pipeline in
            'tokenize_model_path': 'C:\\1Vadim\IT\\Repositories\\KURSACH\\Project\\stanfordnlp\\stanfordnlp_resources\\ru_syntagrus_models\\ru_syntagrus_tokenizer.pt',
            'pos_model_path': 'C:\\1Vadim\IT\\Repositories\\KURSACH\\Project\\stanfordnlp\\stanfordnlp_resources\\ru_syntagrus_models\\ru_syntagrus_tagger.pt',
            'pos_pretrain_path': 'C:\\1Vadim\IT\\Repositories\\KURSACH\\Project\\stanfordnlp\\stanfordnlp_resources\\ru_syntagrus_models\\ru_syntagrus.pretrain.pt',
            'lemma_model_path': 'C:\\1Vadim\IT\\Repositories\\KURSACH\\Project\\stanfordnlp\\stanfordnlp_resources\\ru_syntagrus_models\\ru_syntagrus_lemmatizer.pt',
            'depparse_model_path': 'C:\\1Vadim\IT\\Repositories\\KURSACH\\Project\\stanfordnlp\\stanfordnlp_resources\\ru_syntagrus_models\\ru_syntagrus_parser.pt',
            'depparse_pretrain_path': 'C:\\1Vadim\IT\\Repositories\\KURSACH\\Project\\stanfordnlp\\stanfordnlp_resources\\ru_syntagrus_models\\ru_syntagrus.pretrain.pt'
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
            token = [token.lemma_ for token in text if not (token.is_punct or token.is_stop)]
            clean_text_list.append(token)

        return clean_text_list

    #Собирает текстовые данные в удобный формат таблицы
    def bag_of_words(self, df):
        text = self.__clean_text(self, df)

        udf = pd.DataFrame(data=text[0], columns=['text'])
        udf = udf['text'].value_counts()

        kdf = pd.DataFrame(columns=['text', 'count'])
        kdf['text'] = udf.index
        kdf['count'] = udf.values
        print(kdf[:20])
        return kdf[:30]