#coding = utf-8
from urllib.parse import urlencode

import requests
import json


def get_city():
    city_source = {}
    data = {
        'actionName':'GetAreasAjax',
        'ajaxProvinceId':0,
        'ajaxCityId':110100,
        'ajaxBrandid':0,
        'ajaxManufactoryid':0,
        'ajaxSeriesid':0
    }
    url = 'http://dealer.autohome.com.cn/Ajax' + '?' + urlencode(data)
    data = json.loads(requests.get(url).text)
    if data and 'AreaInfoGroups' in data.keys():
        for item in data.get('AreaInfoGroups'):
            for it in item.get('Values'):
                yield  {
                    'url': 'http://dealer.autohome.com.cn/' + it.get('Pinyin'),
                    'count' : it.get('Count'),
                }


if __name__ == '__main__':

    get_city()