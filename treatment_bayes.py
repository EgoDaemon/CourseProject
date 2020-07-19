import numpy as np
import pandas as pd
import sqlite3
from sqlalchemy import Column
import re

from preprocessing import preprocessing
import joblib

import matplotlib.pyplot as plt

conn = sqlite3.connect("our_db.db")

cursor=conn.cursor()
sql = """select comment from VK_comments limit 20;"""
l=[]
try:   
    cursor.execute(sql)
    rs = cursor.fetchall()    
    for i in rs:     
        k=list(i)      
        l.append(k[0])
    conn.commit()
except:
    conn.rollback()
conn.close()
# print(l)

data = [preprocessing(words) for words in l]
print(data)

clf = joblib.load('bayes.pkl')
prediction = clf.predict(data)
print(prediction)

pd.DataFrame(prediction).to_csv("res_with_pd.csv", header=None, index=None)

# connection = sqlite3.connect("our_db.db")
# cursor = connection.cursor()
# cursor.execute("alter table VK_comments add column 'Result' 'integer'")
# connection.commit()
# connection.close()

df =  pd.read_csv('res_with_pd.csv', encoding='UTF-8', names=['N'], header=1)

# print(df.shape)
# print(df.describe())

filters_1 = df['N'] <= 0
a = len(df.loc[filters_1])
print('Негативных комментариев:', a)
filters_2 = df['N'] <= 1
b = len(df.loc[filters_2])
print('Позитивных комментариев:', b)
A1 = a/(a+b)
A2 = b/(a+b)

labels = 'Negative', 'Positive'
sizes = [A1, A2]
fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
ax1.axis('equal')
plt.show()