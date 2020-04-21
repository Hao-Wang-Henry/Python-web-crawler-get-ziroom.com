import base64
import urllib
from typing import BinaryIO
from urllib.parse import urlencode
from urllib import request
import requests
from urllib.request import urlopen
import json
import ssl
from skimage import io
import cv2

# 配置百度服务
ssl._create_default_https_context = ssl._create_unverified_context
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&' \
       'client_id=【你的API Key】&client_secret=【你的Secret Key】'
headers = {'Content-Type': 'application/json;charset=UTF-8'}
res = requests.get(url=host, headers=headers).json()
access_token=res['access_token']
url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token=' + access_token


img_link = "static8.ziroom.com/phoenix/pc/images/2019/price/234a22e00c646d0a2c20eccde1bbb779.png"

# 从网页上下载原图
image = io.imread("http://" + img_link)
io.imsave('tem.png', image)
# 百度说jpg的精度更高
image = cv2.imread('tem.png')
cv2.imwrite("tem.jpg", image)
# 处理图片，上传到百度
f: BinaryIO = open(r'tem.jpg', 'rb')
op: bytes = f.read()
imgR = base64.b64encode(op)
params = {'image': imgR}
params2 = urllib.parse.urlencode(params).encode(encoding='UTF8')
request1 = request.Request(url, params2)
request1.add_header('Content-Type', 'application/x-www-form-urlencoded')
response = urlopen(request1)
# 百度处理图片
content: object = response.read()
result: object = content.decode()
json1 = json.loads(result)
jsonArray = json1['words_result']
price_array = jsonArray[0]['words']
print(price_array)
