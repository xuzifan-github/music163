# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MusicItem(scrapy.Item):
    music_id = scrapy.Field()
    title = scrapy.Field()
    cover = scrapy.Field()
    tag = scrapy.Field()
    lyric = scrapy.Field()
    album = scrapy.Field()
    artist = scrapy.Field()


class CommentItem(scrapy.Item):
    music_id = scrapy.Field()
    user_id = scrapy.Field()
    nickname = scrapy.Field()
    avatar_url = scrapy.Field()
    content = scrapy.Field()
    comment_time = scrapy.Field()
    liked_count = scrapy.Field()
    content_md5 = scrapy.Field()


class MusicFileItem(scrapy.Item):
    music_id = scrapy.Field()
    download_url = scrapy.Field()
    file_size = scrapy.Field()
    file_path = scrapy.Field()
