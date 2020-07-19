# import os
# import sqlalchemy
# import sys

from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import parser
from parser import access_token, api_version, offset, count
# os.remove(r"db_test2.db")


engine = create_engine('sqlite:///vkapp.db', echo=True)
"""выбираем, с какой базой хотим работать (sqlite)
и в какой файлик записываем"""
Base = declarative_base()
"""говорим, что это будет декларативный mapping (он удобнее)"""


class Posts(Base):  # делаем табличку с полями для постов
    __tablename__ = 'VK_posts'
    id = Column(Integer, primary_key=True)
    id_post = Column(Integer)
    likes = Column(Integer)
    pics = Column(Boolean)
    post = Column(String, nullable=False)
    date = Column(DateTime)


class Comments(Base):  # делаем табличку с полями для комментов
    __tablename__ = 'VK_comments'
    id = Column(Integer, primary_key=True)
    id_post = Column(Integer)
    id_comm = Column(Integer)
    comment = Column(String)
    num_likes = Column(Integer)
    date = Column(DateTime)


Base.metadata.drop_all(engine)   # очищаем файлик от прежних данных
Base.metadata.create_all(engine)
session = sessionmaker(bind=engine)()


def save_all(records):
    session.add(records)
    session.new
    session.commit()


def collect_posts(domain):
    posts = parser.posts_collector(access_token, api_version,
                                   offset, count, domain)
    return posts


def save_posts(posts):
    for entity in posts:
        all_posts = Posts(id_post=entity['id'],
                          likes=entity['post_likes'],
                          post=entity['text'],
                          date=datetime.strptime(entity['date'], '%d/%m/%y %H:%M'),
                          pics=entity['post_pics'],
                          )
        save_all(all_posts)
    return posts


def collect_comments(posts):
    # post = input('введите номер поста: ')
    # post = 572920
    comments_dirty = parser.comments_collector(posts, access_token,
                                               api_version, offset, None)
    comms_clean = parser.comms_without_emoji(comments_dirty)
    return comms_clean


def save_comments(comments):
    for comment in comments:
        all_comment = Comments(id_post=comment['post_id'],
                               id_comm=comment['id_comm'],
                               comment=comment['comms'],
                               num_likes=comment['count_likes'],
                               date=datetime.strptime(comment['date'],
                                                    '%d/%m/%y %H:%M'),
                               )   
        save_all(all_comment)


# posts = collect_posts('potomuchtoludi')
# save_posts(posts)
# comments = collect_comments(posts)
# save_comments(comments)
