from urllib.parse import urlencode
import requests
from lxml import etree
from multiprocessing import Pool
from get_city import get_city
import math
import time
import pymongo
from config import *

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

def save_to_mongodb(data):
    if db[MONGO_TABLE].insert(data):
        print('存储到Mongodb成功',data)
        return True
    return False


def get_content(html,page):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Referer': 'http://dealer.autohome.com.cn/'
    }

    p = math.ceil(page/15)
    content = {}
    for i in range(1,p):
        data = {
            'countyId': 0,
            'brandId': 0,
            'seriesId': 0,
            'factoryId': 0,
            'pageIndex': i,
            'kindId': 1,
            'orderType': 0,
        }
        url = html + '?' + urlencode(data)
        wb_data = etree.HTML(requests.get(url,headers).text)
        item_list = wb_data.xpath('//li[@class="list-item"]')
        for item in item_list:
            data = {
                'name':item.xpath('.//li[@class="tit-row"]/a/span/text()')[0],
                'type': item.xpath('.//li[@class="tit-row"]/span[@class="green"]/text()')[0],
                'id':item.xpath('.//li[@class="tit-row"]/a/@href')[0].split('/')[3],
                'pinpai': item.xpath('.//ul[@class="info-wrap"]/li[2]/span/em/text()')[0],
                'tel': item.xpath('.//ul[@class="info-wrap"]/li[3]/span[@class="tel"]/text()')[0],
                'time': item.xpath('.//ul[@class="info-wrap"]/li[3]/span[@class="gray"]/text()')[0] if item.xpath('.//span[@class="gray"]') else None,
                'adress': item.xpath('.//ul[@class="info-wrap"]/li[4]/span[@class="info-addr"]/text()')[0],
            }
            print(data)
            save_to_mongodb(data)




if __name__ == '__main__':
    pool = Pool()
    city_list = get_city()
    for item in city_list:
        pool.apply_async(get_content,args=(item['url'],item['count']))
    pool.close()
    pool.join()

