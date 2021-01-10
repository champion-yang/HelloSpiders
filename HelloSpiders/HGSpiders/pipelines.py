from HelloSpiders.database.dao import *

class HgspidersPipeline:
    def process_item(self, item, spider):
        return item

class JueJinPipeline():
    # def __init__(self, Session):
    #     self.Session = Session
    #
    # @classmethod
    # def from_crawler(cls, crawler):
    #     from sqlalchemy.orm import sessionmaker
    #     from HelloSpiders.database.sqlmy_db import engine
    #     Session = sessionmaker(bind=engine)
    #
    #     return cls(
    #         Session=Session
    #     )
    #
    # def open_spider(self, spider):
    #     self.session = self.Session()
    #
    # def close_spider(self, spider):
    #     self.session.close()

    def process_item(self, item, spider):
        data = dict(item)
        if not data:
            return data
        if data.get('item_type') == 1:
            insert_or_update_source(data)
        elif data.get('item_type') == 2:
            insert_or_update_article(data)

        return item
