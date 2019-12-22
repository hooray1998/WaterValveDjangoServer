# -*- coding:utf-8 -*-

import requests
import json

#url = 'http://0.0.0.0:8000/bindPhone?openid=openid3&phone=141'
# url = 'http://0.0.0.0:8000/addDevice?phone=131&serial_num=se2&source=0'
# url = 'http://0.0.0.0:8000/userDevices?phone=151'
# url = 'http://0.0.0.0:8000/delDevice?phone=151&device_id=6'
# url = 'http://0.0.0.0:8000/userDevice?phone=151&device_id=6'
url = 'http://0.0.0.0:8000/openDegree?phone=151&device_id=6&number=7'
r = requests.get(url)
print(json.dumps(json.loads(r.text),indent=4))
