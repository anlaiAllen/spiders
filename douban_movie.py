import json

import requests
import re
from requests.exceptions import RequestException
from multiprocessing import Pool

def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return "请求失败"
    except RequestException as e:
        return  e

def parse_page(text):
    patter = re.compile('<li>.*?<em.*?>(\d+)</em>.*?<span.*?title">(.*?)</span>.*?<p.*?>(.*?)&nbsp;&nbsp;&nbsp;(.*?)<br>(.*?)&nbsp;/&nbsp;'
                        +'(.*?)&nbsp;/&nbsp;(.*?)</p>.*?v:average">(.*?)</span>.*?</span>.*?>(.*?)</span>'
                         +'.*?inq">(.*?)</span>',re.S)
    items = re.findall(patter , text)
    for item in items:
        yield {
            'rank' : item[0],
            'name' : item[1],
            'director' : item[2].strip()[3:].split('/'),
            'actor' : item[3].strip()[3:].split('/'),
            'data' : item[4].strip(),
            'county' : item[5],
            'type' : item[6].strip(),
            'score' : item[7],
            'comment' : item[8][:-3],
            'paragraph' : item[9].strip()
        }

def write2text(content):
    with open('douban_top250.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False) + '\n')




def main(offest):
    url = 'https://movie.douban.com/top250?start=' + str(offest)
    html = get_one_page(url)
    for item in parse_page(html):
        print(item)
        write2text(item)


if __name__ == '__main__':
    p = Pool()
    for i in range(10):
        p.apply_async(main,args=(i*25,))
    p.close()
    p.join()