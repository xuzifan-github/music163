# -*- coding: utf-8 -*-
import base64
import codecs
import json
import os
import urllib.request
import music163.database as db
from Crypto.Cipher import AES
from scrapy import Spider, FormRequest
from music163.items import MusicFileItem

cursor = db.connection.cursor()


def to_16(key):
    while len(key) % 16 != 0:
        key += '\0'
    return str.encode(key)


def AES_encrypt(text, key, iv):
    bs = AES.block_size
    pad2 = lambda s: s + (bs - len(s) % bs) * chr(bs - len(s) % bs)
    encryptor = AES.new(to_16(key), AES.MODE_CBC, to_16(iv))
    encrypt_aes = encryptor.encrypt(str.encode(pad2(text)))
    encrypt_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')
    return encrypt_text


def RSA_encrypt(text, pubKey, modulus):
    text = text[::-1]
    rs = int(codecs.encode(text.encode('utf-8'), 'hex_codec'), 16) ** int(pubKey, 16) % int(modulus, 16)
    return format(rs, 'x').zfill(256)


class MovieMetaSpider(Spider):
    music_file_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + '/music'
    if not os.path.exists(music_file_dir):
        os.mkdir(music_file_dir)
    song_url = 'https://music.163.com/weapi/song/enhance/player/url?csrf_token='
    g = '0CoJUm6Qyw8W8jud'
    b = "010001"
    c = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
    i = 'dStl00zDO2XwAaTg'
    iv = "0102030405060708"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        'Referer': 'https://music.163.com/',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    name = 'download'
    allowed_domains = ['163.com']
    sql = 'SELECT music_id,title,artist FROM music WHERE music_id NOT IN \
            (SELECT music_id FROM music_file) ORDER BY music_id DESC'
    cursor.execute(sql)
    musics = cursor.fetchall()

    def start_requests(self):
        for music in self.musics:
            music_id = music['music_id']
            title = music['title']
            artist = music['artist']
            file_name = f'{artist} - {title}'
            formdata = {
                'params': self.get_params(music_id),
                'encSecKey': self.get_encSecKey()
            }
            yield FormRequest(self.song_url, formdata=formdata, meta={'music_id': music_id, 'file_name': file_name},
                              callback=self.download_mp3, headers=self.headers)

    def download_mp3(self, response):
        music_id = response.meta['music_id']
        file_name = response.meta['file_name']
        download_url = json.loads(response.text)["data"][0]["url"]
        if download_url:
            file_path = self.music_file_dir + '/' + file_name + '.mp3'
            urllib.request.urlretrieve(download_url, file_path)
            file_size = '%.2f MB' % (os.path.getsize(file_path) / 1024 / 1024)
            item = MusicFileItem()
            item['music_id'] = music_id
            item['download_url'] = download_url
            item['file_size'] = file_size
            item['file_path'] = file_path.replace('\\', '/')
            yield item

    def get_params(self, music_id):
        encText = str({'ids': "[" + str(music_id) + "]", 'br': 128000, 'csrf_token': ""})
        return AES_encrypt(AES_encrypt(encText, self.g, self.iv), self.i, self.iv)

    def get_encSecKey(self):
        return RSA_encrypt(self.i, self.b, self.c)
