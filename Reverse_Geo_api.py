import requests
import xml.etree.ElementTree as ET
import pprint

def return_locate_to_adress(lat , lon):
    appID=""

    url = f"https://map.yahooapis.jp/geoapi/V1/reverseGeoCoder?lat={lat}&lon={lon}&appid={appID}"

    response = requests.get(url)
    xml_data=response.content

    root = ET.fromstring(xml_data)
    ns = {'y': 'http://olp.yahooapis.jp/ydf/1.0'}
    address = root.find(".//y:Address", ns).text
    print(f"{address}の天気予報は以下の通りです。\n")
