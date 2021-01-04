# coding=utf-8
"""
@auth: xiaobei
@date: 2020/01/03
@desc: 时间紧急，凑合着用吧～
"""
from HelloSpiders.database import sqlmy_db
from sqlalchemy.orm import sessionmaker
import logging
import datetime


def insert_or_update_source(**kwargs):
    session_class = sessionmaker(bind=sqlmy_db.engine)
    session = session_class()
    result = session.query(sqlmy_db.SourceInfo).filter_by(source_name=kwargs['source_name']).first()
    if not result:
        try:
            sqlmy_pdf = sqlmy_db.SourceInfo(
                source_name=kwargs['source_name'],
                blogger_name=kwargs['blogger_name'],
                followee_count=kwargs['followee_count'],
                follower_count=kwargs['follower_count'],
                post_article_count=kwargs['post_article_count'],
                got_digg_count=kwargs['got_digg_count'],
                got_view_count=kwargs['got_view_count'],
                c_time=datetime.datetime.now()
            )
            session.add(sqlmy_pdf)
        except Exception as e:
            logging.error(f'save to mysql failed! error msg:{e}')
    else:
        session.query(sqlmy_db.SourceInfo).filter_by(source_name=kwargs['source_name']).update(
            {
                "source_name": kwargs['source_name'],
                "blogger_name": kwargs['blogger_name'],
                "followee_count": kwargs['followee_count'],
                "follower_count": kwargs['follower_count'],
                "post_article_count": kwargs['post_article_count'],
                "got_digg_count": kwargs['got_digg_count'],
                "got_view_count": kwargs['got_view_count'],
                "u_time": datetime.datetime.now()
            }
        )
    session.commit()
    session.close()


def insert_or_update_article(**kwargs):
    session_class = sessionmaker(bind=sqlmy_db.engine)
    session = session_class()
    result = session.query(sqlmy_db.ArticleInfo).filter_by(article_id=kwargs['article_id']).first()
    if not result:
        try:
            source_info = session.query(sqlmy_db.SourceInfo).filter_by(source_name=kwargs['source_name']).first()
            if source_info:
                sqlmy_pdf = sqlmy_db.ArticleInfo(
                    article_id=kwargs['article_id'],
                    source_id=source_info['source_id'],
                    article_link=kwargs['article_link'],
                    title=kwargs['title'],
                    is_original=kwargs['is_original'],
                    view_count=kwargs['view_count'],
                    collect_count=kwargs['collect_count'],
                    diff_count=kwargs['diff_count'],
                    comment_count=kwargs['comment_count'],
                    category_name=kwargs['category_name'],
                    tags=kwargs['tags'],
                    article_ctime=kwargs['article_ctime'],
                    article_utime=kwargs['article_utime'],
                    c_time=datetime.datetime.now()
                )
                session.add(sqlmy_pdf)
                session.commit()
            else:
                logging.error(f'not found {kwargs["source_name"]}, please insert into {kwargs["source_name"]}, then try again!')
        except Exception as e:
            logging.error(f'save to mysql failed! error msg:{e}')
    else:
        session.query(sqlmy_db.ArticleInfo).filter_by(article_id=kwargs['article_id']).update(
            {
                "title": kwargs['title'],
                "view_count": kwargs['view_count'],
                "collect_count": kwargs['collect_count'],
                "comment_count": kwargs['comment_count'],
                "diff_count": kwargs['diff_count'],
                "article_utime": datetime.datetime.now(),
                "u_time": datetime.datetime.now()
            }
        )
    session.close()


if __name__ == '__main__':
    pass
