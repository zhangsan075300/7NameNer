# import geopy
import json
from urllib.request import urlopen
import urllib.parse as urp
def getlnglat(address):
    """
    用百度api，返回的只能是国内的坐标
    :param address: 输入中文
    :return:返回json数据
    """
    address1 = address
    url = 'http://api.map.baidu.com/geocoding/v3/'
    output = 'json'
    ak = 'oUbPUoTmVebpx0OR92akkQQeCK6nTvt5'
    address = urp.quote(address)
    uri = url + '?' + 'address=' + address + '&output=' + output + '&ak=' + ak
    req = urlopen(uri)
    res = req.read().decode()
    temp = json.loads(res)
    if temp['status'] == 0:
        lat = temp['result']['location']['lat']
        lng = temp['result']['location']['lng']
        dict_data = {
            "name": address1,
            "lng": lng,
            "lat": lat
        }
        print(dict_data)
        return dict_data   # 纬度 latitude   ，   经度 longitude  ，
    if temp['status'] == 1:
        dict_data = {
            "name": address1,
        }
        print(dict_data)
        return dict_data

def geo(address):
    """
    将查询地理定位到地址和坐标,用bing的key，百度的key
    """
    from geopy.geocoders import Bing, GoogleV3, DataBC, Nominatim
    geolocator = Bing('Ah0z5jRxM7zVthdYGas9JqAHBaXdMYjys9P5qls3ZAUnpu73YvweIjU8T1GOS0Gq')
    # geolocator = GoogleV3('AIzaSyAVwjaaOBKbssuyQsvyqQAQDwfuzO1PKCA')

    location = geolocator.geocode(address)
    lat = location.latitude
    lng = location.longitude
    dict_data = {
        "name": address,
        "lng": str(lng),
        "lat": str(lat)
    }
    return dict_data

def readfromjson(word):
    with open("./data/location.json",'r',encoding='utf-8')as f:
        json_data = json.load(f)
        for line in json_data:
            if line['location_zh'] == word:
                lat = line['lat']
                lng = line['lng']
                dict_data = {
                    "name": line['location_zh'],
                    "lng": lat,
                    "lat": lng
                }
                print(dict_data)
                return (dict_data)

