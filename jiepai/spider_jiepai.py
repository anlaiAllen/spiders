import json
from json import JSONDecodeError
from urllib.parse import urlencode
import multiprocessing
import re
import requests
from bs4 import BeautifulSoup
from requests import RequestException
from config import *
import pymongo

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]


def get_index(offset,keyword):
    data = {
        'offset':offset,
        'format':'json',
        'keyword':keyword,
        'autoload':'true',
        'count':'20',
        'ur_tab':3
    }
    url = 'https://www.toutiao.com/search_content/?' + urlencode(data)
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.text
        return None
    except RequestException as e:
        print('访问索引页失败',e)
        return None

def parse_index(html):
    try:
        r = json.loads(html)
        if r and 'data' in r.keys():
            for item in r.get('data'):
                yield item.get('article_url')
    except JSONDecodeError:
        pass

def get_url_detail(url):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.text
        return None
    except RequestException as e:
        print('请求详情页失败',e)
        return None

def parse_url_detail(html,url):
    soup = BeautifulSoup(html,'lxml')
    title = soup.select('title')[0].get_text()
    images_patten = re.compile('var gallery = (.*?);',re.S)
    images = re.search(images_patten,html)
    if  images:
        data = json.loads(images.group(1))
        if data and 'sub_images' in data.keys():
            img = [item.get('url') for item in data.get('sub_images')]
            return {
                'title':title,
                'img':img,
                'url':url
            }
def save_to_mongodb(data):
    if db[MONGO_TABLE].insert(data):
        print('存储到Mongodb成功',data)
        return True
    return False


if __name__ == '__main__':
    for i in range(0,200,20):
        html = get_index(i,'街拍')
        for url in parse_index(html):
            html = get_url_detail(url)
            if html:
                result = parse_url_detail(html,url)
                if result:
                    save_to_mongodb(result)

