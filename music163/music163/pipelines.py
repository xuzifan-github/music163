# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import music163.database as db
from music163.items import MusicItem, CommentItem

cursor = db.connection.cursor()


class Music163Pipeline(object):
    def get_music(self, item):
        sql = 'SELECT id FROM music WHERE music_id=%s' % item['music_id']
        cursor.execute(sql)
        return cursor.fetchone()

    def save_music(self, item):
        keys = item.keys()
        values = tuple(item.values())
        fields = ','.join(keys)
        temp = ','.join(['%s'] * len(keys))
        sql = 'INSERT INTO music (%s) VALUES (%s)' % (fields, temp)
        cursor.execute(sql, values)
        return db.connection.commit()

    def get_comment(self, item):
        sql = 'SELECT id FROM comments WHERE content_md5="%s"' % item['content_md5']
        cursor.execute(sql)
        return cursor.fetchone()

    def save_comment(self, item):
        keys = item.keys()
        values = tuple(item.values())
        fields = ','.join(keys)
        temp = ','.join(['%s'] * len(keys))
        sql = 'INSERT INTO comments (%s) VALUES (%s)' % (fields, temp)
        cursor.execute(sql, values)
        return db.connection.commit()

    def save_music_file(self, item):
        keys = item.keys()
        values = tuple(item.values())
        fields = ','.join(keys)
        temp = ','.join(['%s'] * len(keys))
        sql = 'INSERT INTO music_file (%s) VALUES (%s)' % (fields, temp)
        cursor.execute(sql, values)
        return db.connection.commit()

    def process_item(self, item, spider):
        if isinstance(item, MusicItem):
            exist = self.get_music(item)
            if not exist:
                try:
                    self.save_music(item)
                except Exception as e:
                    print(item)
                    print(e)
        elif isinstance(item, CommentItem):
            exist = self.get_comment(item)
            if not exist:
                try:
                    self.save_comment(item)
                except Exception as e:
                    print(item)
                    print(e)
        else:
            try:
                self.save_music_file(item)
            except Exception as e:
                print(item)
                print(e)
        return item
