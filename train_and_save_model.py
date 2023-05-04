from collections import defaultdict

import gensim
from gensim.models import FastText
import pandas as pd
import numpy as np
import pymorphy2
import nltk  # Natural Language Toolkit - для загрузки стоп слов русского языка
import re

from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score, classification_report
from tqdm import tqdm  # прогресбарbincount
from sklearn.pipeline import Pipeline

from sklearn.model_selection import train_test_split  # рабиваем данные на traint и test

regex = re.compile(r'[А-Яа-яA-zёЁ-]+')


class TfidfEmbeddingVectorizer(object):
    def __init__(self, word2vec):
        self.word2vec = word2vec
        self.word2weight = None
        self.dim = len(w2v.popitem()[1])

    def fit(self, X, y):
        tfidf = TfidfVectorizer(analyzer=lambda x: x)
        tfidf.fit(X)
        max_idf = max(tfidf.idf_)
        self.word2weight = defaultdict(
            lambda: max_idf,
            [(w, tfidf.idf_[i]) for w, i in tfidf.vocabulary_.items()])

        return self

    def transform(self, X):
        return np.array([
            np.mean([self.word2vec[w] * self.word2weight[w]
                     for w in words if w in self.word2vec] or
                    [np.zeros(self.dim)], axis=0)
            for words in X
        ])


def words_only(text, regex=regex):
    try:
        return " ".join(regex.findall(text)).lower()
    except Exception as e:
        return ""


def process_data(data, all_stop_words) -> []:
    word_tokenizer = nltk.WordPunctTokenizer()

    texts = []
    targets = []

    # инициализируем лемматизатор
    morph = pymorphy2.MorphAnalyzer()

    # поочередно проходим по всем новостям в списке
    for item in tqdm(data):
        text_lower = words_only(item)  # оставим только слова
        tokens = word_tokenizer.tokenize(text_lower)  # разбиваем текст на слова

        # удаляем пунктуацию и стоп-слова, а так же лемитизируем  слова
        tokens = [morph.parse(word)[0].normal_form for word in tokens if
                  (word not in all_stop_words and not word.isnumeric())]

        # texts.append(tokens) # добавляем в предобработанный список
        texts.append(' '.join(tokens))

    return texts


def save_prepared_dataset(file_name, texts):
    with open(file_name, 'w', encoding='utf-8') as file:
        for line in texts:
            file.write(line + '\n')
        file.flush()


def read_prepared_datasets(file_name) -> []:
    result = []
    with open(file_name, 'r', encoding='utf-8') as file:
        for line in file.readlines():
            result.append(line.replace('\n', ''))
    return result


if __name__ == '__main__':
    prepared_dataset_file_name = 'dataset/prepared_dataset.txt';

    # загружаем список стоп-слов для русского
    nltk.download('stopwords')
    stop_words = nltk.corpus.stopwords.words('russian')

    # расширим список стоп-слов, словами, которые являеются стоп-словами в данной задаче
    add_stop_words = ['ао', 'оао', 'ооо']
    months = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь',
              'декабрь', ]
    all_stop_words = stop_words + add_stop_words + months

    df = pd.read_csv('dataset/dataset.csv', sep=',', engine='python')

    y = df['title'].tolist()
    texts = process_data(df['text'].tolist(), all_stop_words)
    print(len(texts))
    save_prepared_dataset(prepared_dataset_file_name, texts)