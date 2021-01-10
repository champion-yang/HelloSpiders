# coding=utf-8
"""
@auth: xiaobei
@date: 2021/1/1
@desc:
"""

import datetime
import sys, pathlib
import time

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
import uuid
from sqlalchemy import create_engine
from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, Boolean, Text, Date, DateTime, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from HelloSpiders.config import service_config

DIALECT = service_config.get('database', 'dialect')
DRIVER = service_config.get('database', 'driver')
USER = service_config.get('database', 'user')
PASSWORD = service_config.get('database', 'password')
HOST = service_config.get('database', 'host')
PORT = service_config.get('database', 'port')
DBNAME = service_config.get('database', 'database_name')
CHARSET = service_config.get('database', 'charset')
ECHO = service_config.get('database', 'echo')
ECHO = True if ECHO == '1' else False
POOL_SIZE = int(service_config.get('database', 'pool_size'))

DBURI = '{}+{}://{}:{}@{}:{}/{}?charset={}'.format(DIALECT, DRIVER, USER, PASSWORD, HOST, PORT, DBNAME, CHARSET) \
    if CHARSET else \
    '{}+{}://{}:{}@{}:{}/{}'.format(DIALECT, DRIVER, USER, PASSWORD, HOST, PORT, DBNAME)
engine = create_engine(DBURI, encoding='utf8', echo=ECHO, pool_size=POOL_SIZE, max_overflow=3, pool_timeout=60)

base = declarative_base()

"""
CREATE TABLE article_info (
	id INT AUTO_INCREMENT COMMENT '自增id',
	source_id INT NOT NULL DEFAULT 0 COMMENT '来源id',
	article_id VARCHAR ( 32 ) DEFAULT NULL COMMENT '目标网站的文章id',
	article_link VARCHAR ( 128 ) DEFAULT NULL COMMENT '目标网站的link链接',
	title VARCHAR ( 128 ) DEFAULT NULL COMMENT '文章标题',
	is_original TINYINT DEFAULT 1 COMMENT '是否原创，1:是，0:否',
	view_count BIGINT DEFAULT 0 COMMENT '阅读量',
	collect_count BIGINT DEFAULT 0 COMMENT '收藏量',
	diff_count BIGINT DEFAULT 0 COMMENT '点赞量',
	comment_count BIGINT DEFAULT 0 COMMENT '评论量',
	category_name VARCHAR ( 32 ) DEFAULT NULL COMMENT '文章所属分类',
	article_ctime datetime COMMENT '文章创建时间',
	article_utime datetime COMMENT '文章更新时间',
	tags VARCHAR ( 128 ) DEFAULT NULL COMMENT '文章标签',
	c_time TIMESTAMP NOT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
	u_time TIMESTAMP NOT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
	PRIMARY KEY ( `id` ),
	KEY `idx_source_id` ( `source_id` )
) ENGINE = INNODB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '文章信息表';

CREATE TABLE source_info (
	id INT AUTO_INCREMENT COMMENT '自增id',
	source_name VARCHAR ( 32 ) DEFAULT NULL COMMENT '来源名字，比如掘金，知乎',
	blogger_name VARCHAR ( 32 ) DEFAULT NULL COMMENT '博主名字',
	followee_count BIGINT DEFAULT 0 COMMENT '关注人数',
	follower_count BIGINT DEFAULT 0 COMMENT '关注者数',
	post_article_count BIGINT DEFAULT 0 COMMENT '发布文章总数',
	got_digg_count BIGINT DEFAULT 0 COMMENT '获得点赞总数',
	got_view_count BIGINT DEFAULT 0 COMMENT '获得阅读总数',
	c_time TIMESTAMP NOT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
	u_time TIMESTAMP NOT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
	PRIMARY KEY ( `id` )
) ENGINE = INNODB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '来源信息表';

"""


class ArticleInfo(base):
    __tablename__ = 'article_info'
    id = Column(Integer, primary_key=True, autoincrement=True)
    source_id = Column(Integer)
    article_id = Column(String(32))
    article_link = Column(String(32))
    title = Column(String(32))
    is_original = Column(Integer)
    view_count = Column(Integer)
    collect_count = Column(Integer)
    diff_count = Column(Integer)
    comment_count = Column(Integer)
    category_name = Column(String(132))
    tags = Column(String(128))
    article_ctime = Column(DateTime, default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    article_utime = Column(DateTime, default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    c_time = Column('c_time', DateTime, default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    u_time = Column('u_time', DateTime, default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    # SQLalchemy要求输入的数据不能比data model中定义的Column多，在此去除
    def __init__(self, **kwargs):
        keep_kwargs = {k: v for k, v in kwargs.items() if k in [field for field in ArticleInfo.__dict__ if not field.startswith('_')]}
        super(ArticleInfo, self).__init__(**keep_kwargs)

    # 自定义输出实例化对象时的信息
    def __repr__(self):
        return 'custom: < meta data(id = {}, article_link = {})>'.format(self.id, self.article_link)

    def to_dict(self):
        return {c: getattr(self, c) for c in self.__dict__}


class SourceInfo(base):
    __tablename__ = 'source_info'

    id = Column(Integer, primary_key=True, autoincrement=True)
    source_name = Column(String(32))
    blogger_name = Column(String(32))
    followee_count = Column(Integer)
    follower_count = Column(Integer)
    post_article_count = Column(Integer)
    got_digg_count = Column(Integer)
    got_view_count = Column(Integer)

    c_time = Column('c_time', DateTime)
    u_time = Column('u_time', DateTime, default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def __init__(self, **kwargs):
        keep_kwargs = {k: v for k, v in kwargs.items() if k in [field for field in SourceInfo.__dict__ if not field.startswith('_')]}
        super(SourceInfo, self).__init__(**keep_kwargs)

    def __repr__(self):
        return 'custom: < meta data(id = {}, source_name = {})>'.format(self.id, self.source_name)

    def to_dict(self):
        return {c: getattr(self, c) for c in self.__dict__}

base.metadata.create_all(engine)


if __name__ == '__main__':
    from sqlalchemy.orm import sessionmaker

    Session = sessionmaker(bind=engine)
    session = Session()
    # d_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # result = session.query(ArticleInfo).filter_by(id=1).update(
    #     {ArticleInfo.c_time: d_time})
    result = session.query(SourceInfo).filter_by(source_name='测试').first()

    #
    # print(result)
    # print(result.to_dict()['source_name'])
    # # print(result['followee_count'])
    # print(dir(result))
    # ctime 也会变
    result = session.query(SourceInfo).filter_by(source_name='测试').update(
        {
            "u_time": datetime.datetime.now()
        }
    )
    session.commit()
    session.close()
