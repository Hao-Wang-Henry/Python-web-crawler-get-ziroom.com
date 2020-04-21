import requests
import re

headers = {
	'User-Agent':''
}

# 手动设置一个连接，用于测试
link = "http://www.ziroom.com/x/722454239.html"
page = requests.get(link, headers = headers)
print(page.text)

if page.text:
	# 价格
	price1 = re.search('Z_price(.*?)服务费另计', page.text, re.S).group(1)
	print(price1)
	price2 = re.findall('background-position:(.*?)px', price1)
	price5 = "/" + re.search('<span>/(.*?)</span>', price1, re.S).group(1)
	price3 = []
	for w in range(len(price2)):
		price3.append(int(float(price2[w]) / -31.24)+1) # 这里加一只是用于解释方便，真正用的时候还是从0开始的
	print("价格矩阵：", price3)
	print("价格单位：", price5)
	# 价格原图
	img_source = re.search('static(.*?)png', price1).group(1)
	img_link = "static" + img_source + "png"
	print("价格参考图：", img_link)

	# 小区
	village1 = re.search('Z_village_info(.*?)/h3', page.text, re.S).group(1)
	village2 = re.search('<h3>(.*?)<', village1, re.S).group(1)
	print("小区：", village2)

	# 信息
	info = re.search('Z_home_b(.*?)tip-tempbox', page.text, re.S).group(1)
	info2 = re.findall('<dd>(.*?)</dd>', info, re.S)
	print("面积：", info2[0])
	print("朝向：", info2[1])
	print("户型：", info2[2])

	# 位置
	loc1 = re.search('Z_home_o(.*?)</li>', page.text, re.S).group(1)
	loc2 = re.search('<span class="ad">(.*?)</span>', loc1, re.S).group(1)
	print("位置：", loc2)
