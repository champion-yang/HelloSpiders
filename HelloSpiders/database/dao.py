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


def insert_or_update_source(kwargs):
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


def insert_or_update_article(kwargs):
    session_class = sessionmaker(bind=sqlmy_db.engine)
    session = session_class()
    result = session.query(sqlmy_db.ArticleInfo).filter_by(article_id=kwargs['article_id']).first()
    if not result:
        try:
            source_info = session.query(sqlmy_db.SourceInfo).filter_by(source_name=kwargs['source_name']).first()
            if source_info:
                sqlmy_pdf = sqlmy_db.ArticleInfo(
                    article_id=kwargs['article_id'],
                    source_id=source_info.id,
                    article_link=kwargs['article_link'],
                    title=kwargs['title'],
                    is_original=kwargs['is_original'],
                    view_count=kwargs['view_count'],
                    collect_count=kwargs['collect_count'],
                    # diff_count=kwargs['diff_count'],
                    comment_count=kwargs['comment_count'],
                    category_name=kwargs['category_name'],
                    tags=kwargs['tags'],
                    article_ctime=datetime.datetime.fromtimestamp(float(kwargs['artical_ctime'])),
                    article_utime=datetime.datetime.fromtimestamp(float(kwargs['artical_utime'])),
                    # article_ctime=datetime.datetime.strptime(str(kwargs['artical_ctime']) + '000', '%Y-%m-%d %H:%M:%S %f'),
                    # article_utime=datetime.datetime.strptime(str(kwargs['artical_utime']) + '000', '%Y-%m-%d %H:%M:%S %f'),
                    # article_utime=str(kwargs['artical_utime']) + '000',
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
                # "diff_count": kwargs['diff_count'],
                "article_utime": datetime.datetime.now(),
                "u_time": datetime.datetime.now()
            }
        )
    session.close()


if __name__ == '__main__':
    data = {'source_name': '掘金', 'artical_id': '6903685160274214920', 'article_link': 'https://juejin.cn/post/6903685160274214920', 'title': '在 GitHub 玩硬件——GitHub 热点速览 Vol.49', 'is_original': 1, 'view_count': 804, 'collect_count': 0, 'comment_count': 0, 'category_name': '开发工具', 'tags': 'GitHub,开源库资讯', 'artical_ctime': '1607389463', 'artical_utime': '1607389681', 'brief_content': '以下内容摘录自微博@HelloGitHub 的 GitHub Trending 及 Hacker News 热帖（简称 HN 热帖），选项标准：新发布 | 实用 | 有趣，根据项目 release 时间分类，发布时间不超过 7 day 的项目会标注 New，无该标志则说明项目 …'}
    insert_or_update_article(data)
