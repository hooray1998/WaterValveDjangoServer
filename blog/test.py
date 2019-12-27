# -*- coding:utf-8 -*-

import requests
import json

host = '192.168.1.101:8000/'
#url = host + 'bindPhone?openid=openid3&phone=141'
# url = host + 'addDevice?phone=131&serial_num=se2&source=0'
# url = host + 'userDevices?phone=151'
# url = host + 'delDevice?phone=151&device_id=6'
# url = host + 'userDevice?phone=151&device_id=6'
url = host + 'openDegree?phone=151&device_id=6&number=7'
r = requests.get(url)
print(json.dumps(json.loads(r.text),indent=4))
