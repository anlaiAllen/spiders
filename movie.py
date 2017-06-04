# --*--encoding = utf-8
import json
import requests
import re
from requests.exceptions import RequestException

def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code ==200:
            return response.text
        return '请求失败'
    except RequestException as e:
        return None

def parse_one_page(text):
    patter = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?title="(.*?)"'
                        +'.*?<p.*?>(.*?)</p>.*?releasetime">(.*?)</p>.*?"integer">(.*?)</i>'
                         +'.*?fraction">(.*?)</i>.*?</dd>',re.S)

    items = re.findall(patter , text)
    for item in items:
        yield {
            'rank': item[0],
            'img' : item[1],
            'title': item[2],
            'actor' : item[3].strip()[3:],
            'data' : item[4][5:],
            'score' : item[5]+item[6]
        }
def write2text(content):
    with open('movie.text','a',encoding='utf-8') as f:
        f.write(json.dumps(content ,ensure_ascii=False) + '\n')




def main(offest):
    url = 'http://maoyan.com/board/4?offset=' + str(offest)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write2text(item)

if __name__ == '__main__':
    for i in range(1,10):
        main(i*10)