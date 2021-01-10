import scrapy


class HgspidersItem(scrapy.Item):

    item_type = scrapy.Field()

    article_id = scrapy.Field()
    article_link = scrapy.Field()
    title = scrapy.Field()
    is_original = scrapy.Field()
    view_count = scrapy.Field()
    collect_count = scrapy.Field()
    digg_count = scrapy.Field()
    comment_count = scrapy.Field()
    category_name = scrapy.Field()
    tags = scrapy.Field()
    artical_ctime = scrapy.Field()
    artical_utime = scrapy.Field()
    # 数据库没加
    brief_content = scrapy.Field()

    source_name = scrapy.Field()
    blogger_name = scrapy.Field()
    followee_count = scrapy.Field()
    follower_count = scrapy.Field()
    post_article_count = scrapy.Field()
    got_digg_count = scrapy.Field()
    got_view_count = scrapy.Field()


