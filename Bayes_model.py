import numpy as np
import pandas as pd

import re

import logging

from sklearn.model_selection import train_test_split
from stop_words import get_stop_words

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import GaussianNB
from mlxtend.preprocessing import DenseTransformer

from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

import joblib

col = ['id', 'tdate', 'tname', 'text', 'ttype', 'trep', 'trtv','tfav',
                          'tstcount', 'tfol', 'tfrien', 'listcount']
a = pd.read_csv("positive.csv", encoding='UTF-8', sep=';', error_bad_lines=False, names=col, usecols=['text'])
b = pd.read_csv("negative.csv", encoding='UTF-8', sep=';', error_bad_lines=False, names=col, usecols=['text'])
size = min(a.shape[0], b.shape[0])
sourse_data = np.concatenate((a['text'].values[:size], b['text'].values[:size]), axis=0)
labels = [1] * size + [0] * size

def preprocessing(sometext):
    text = sometext.lower().replace("ё", "е")
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', ' ', text)
    text = re.sub('@[^\s]+', ' ', text)
    text = re.sub('[^a-zA-Zа-яА-Я1-9]+', ' ', text)
    text = re.sub(' +', ' ', text)
    return text.strip()

data = [preprocessing(words) for words in sourse_data]

# print(data[:5])
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
stop_words_voc = get_stop_words('russian')
# tokenize = nltk.data.load('russian.pickle')
inputs_train, inputs_test, expected_output_train, expected_output_test = train_test_split(data, labels, test_size=0.2, random_state=0)

text_model = Pipeline([
                     ('tfidf', TfidfVectorizer(encoding='utf-8', max_features=2000, min_df=7, max_df=0.8, use_idf=True, stop_words = stop_words_voc)),
                     ('to_dense', DenseTransformer()),
                     ('model', GaussianNB(priors=None, var_smoothing=1e-09))
                     ])
text_classifier = text_model.fit(inputs_train, expected_output_train)
predictions = text_classifier.predict(inputs_test)
res1 = text_classifier.predict(['смерть'])
res2 = text_classifier.predict(['любовь'])
print(res1, res2)
print(predictions[:22])
print(accuracy_score(predictions, expected_output_test))

""" сохранение """
# save = joblib.dump(text_model, 'bayes.pkl')
""" загрузка """
# clf = joblib.load('bayes.pkl')