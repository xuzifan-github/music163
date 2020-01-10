# -*- coding: utf-8 -*-
import json
import re
import time
from hashlib import md5
from scrapy import Spider, Request
from music163.items import MusicItem, CommentItem


class MusicSpider(Spider):
    name = 'music'
    allowed_domains = ['163.com']
    base_url = 'https://music.163.com'
    ids = ['1001', '1002', '1003', '2001', '2002', '2003', '6001', '6002', '6003', '7001', '7002', '7003', '4001',
           '4002', '4003']
    initials = [i for i in range(65, 91)] + [0]

    def start_requests(self):
        for id in self.ids:
            for initial in self.initials:
                url = '{url}/discover/artist/cat?id={id}&initial={initial}'.format(url=self.base_url, id=id,
                                                                                   initial=initial)
                yield Request(url, callback=self.parse_index)

    # 获得所有歌手的url
    def parse_index(self, response):
        for sel in response.xpath(
                '//*[@id="m-artist-box"]/li/*'):  # 网易云音乐的歌手页有两个组成部分，上方十个带头像的热门歌手和下方只显示姓名的普通歌手，原来的xpath选择器只能得到热门歌手id,现已修改
            artist = sel.re('href\=\"\/artist\?id\=[(0-9)]{4,9}')
            for artistid in artist:
                artist_url = self.base_url + '/artist' + '/album?' + artistid[14:]
                yield Request(artist_url, callback=self.parse_artist_pre)

    def parse_artist_pre(self, response):
        # 获取第一页专辑的链接
        albums = response.xpath('//*[@id="m-song-module"]/li/div/a[@class="msk"]/@href').extract()
        for album in albums:
            album_url = self.base_url + album
            yield Request(album_url, callback=self.parse_album)
        # 得到专辑页的翻页html elements列表,若不为空，即该歌手专辑存在分页
        artist_albums = response.xpath('//*[@class="u-page"]/a[@class="zpgi"]/@href').extract()
        if artist_albums:
            for artist_album in artist_albums:
                artist_album_url = self.base_url + artist_album
                yield Request(artist_album_url, callback=self.parse_artist)

    # 获得所有歌手专辑的url
    def parse_artist(self, response):
        albums = response.xpath('//*[@id="m-song-module"]/li/div/a[@class="msk"]/@href').extract()
        for album in albums:
            album_url = self.base_url + album
            yield Request(album_url, callback=self.parse_album)

    # 获得所有专辑音乐的url
    def parse_album(self, response):
        musics = response.xpath('//ul[@class="f-hide"]/li/a/@href').extract()
        for music in musics:
            music_id = int(music[9:])
            music_url = self.base_url + music
            yield Request(music_url, meta={'music_id': music_id}, callback=self.parse_music)

    # 获得音乐信息
    def parse_music(self, response):
        music_id = response.meta['music_id']
        title = response.xpath('//div[@class="tit"]/em[@class="f-ff2"]/text()').extract_first()
        cover = response.xpath('//img[@class="j-img"]/@data-src').extract_first()
        artist = response.xpath('//div[@class="cnt"]/p[1]/span/a/text()').extract_first()
        album = response.xpath('//div[@class="cnt"]/p[2]/a/text()').extract_first()
        music_item = MusicItem()
        music_item['music_id'] = music_id
        music_item['title'] = title
        music_item['tag'] = title
        music_item['cover'] = cover
        music_item['artist'] = artist
        music_item['album'] = album
        lrc_url = 'http://music.163.com/api/song/lyric?' + 'id=' + str(music_id) + '&lv=1&kv=1&tv=-1'
        yield Request(lrc_url, meta={'music_item': music_item}, callback=self.get_lyric)
        comment_urls = [
            f'http://music.163.com/api/v1/resource/comments/R_SO_4_{music_id}',
            f'http://music.163.com/api/v1/resource/comments/R_SO_4_{music_id}?limit=60&offset=1',
        ]
        for comment_url in comment_urls:
            yield Request(comment_url, meta={'music_id': music_id}, callback=self.parse_comment)

    def get_lyric(self, response):
        json_data = json.loads(response.text)
        try:
            lrc = json_data['lrc']['lyric']
        except:
            lyric = ''
        else:
            pat = re.compile(r'\[.*\]')
            lrc = re.sub(pat, "", lrc).strip()
            lyric = '\n'.join(i.strip() for i in lrc.split('\n') if i)
        music_item = response.meta['music_item']
        music_item['lyric'] = lyric
        yield music_item

    def parse_comment(self, response):
        music_id = response.meta['music_id']
        result = json.loads(response.text)
        if 'hotComments' in result.keys():
            comment_list = result['hotComments']
        else:
            comment_list = result['comments']
        for comment in comment_list:
            liked_count = comment['likedCount']
            if liked_count <= 15:
                continue
            content = comment['content']
            if len(content) <= 15:
                continue
            user_id = comment['user']['userId']
            nickname = comment['user']['nickname']
            avatar_url = comment['user']['avatarUrl']
            comment_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(comment['time'] / 1000)))
            content_md5 = md5(content.encode('utf-8')).hexdigest()
            comment_item = CommentItem()
            comment_item['music_id'] = music_id
            comment_item['user_id'] = user_id
            comment_item['nickname'] = nickname
            comment_item['avatar_url'] = avatar_url
            comment_item['content'] = content
            comment_item['comment_time'] = comment_time
            comment_item['liked_count'] = liked_count
            comment_item['content_md5'] = content_md5
            yield comment_item
