# 任务：爬自如上面北京的租房数据，包括小区，面积，朝向，区域，租金，大致位置（比如距离某地铁站多少米）这些信息

import requests
import re
import base64
import urllib
from typing import BinaryIO
from urllib.parse import urlencode
from urllib import request
from urllib.request import urlopen
import json
import ssl
from skimage import io
import cv2
import xlwt

# 配置百度服务
ssl._create_default_https_context = ssl._create_unverified_context
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&' \
       'client_id=【你的API Key】&client_secret=【你的Secret Key】'
headers1 = {'Content-Type': 'application/json;charset=UTF-8'}
res = requests.get(url=host, headers=headers1).json()
access_token = res['access_token']
url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token=' + access_token
# 配置浏览器
headers = {
    'User-Agent': ''
                  ''
}
# 手动分出来北京的区域
district = ['d23008614', '东城', 'd23008626', '西城', 'd23008613', '朝阳', 'd23008618', '海淀', 'd23008617', '丰台',
            'd23008623', '石景山', 'd23008625', '通州', 'd23008611',  '昌平', 'd23008615', '大兴',
            'd23008629', '亦庄开发区', 'd23008624', '顺义', 'd23008616', '房山', 'd23008620', '门头沟']
# 所有连接存到一张空表格里面去
All_links = []
All_link = []
# 生成两个空表格
heads = ["序号", "链接", "价格", "区域", "小区", "面积", "户型", "朝向", "大致位置"]
Beijing = xlwt.Workbook(encoding="utf-8", style_compression=0)
Error = xlwt.Workbook(encoding="utf-8", style_compression=0)
sheet = Beijing.add_sheet("Beijing", cell_overwrite_ok=True)
error_sheet = Error.add_sheet("Beijing", cell_overwrite_ok=True)

# 给表格写表头并存下来
index = 0
error_index = 0
error_sheet.write(error_index, 0, "异常类型")
for i in range(len(heads)):
    sheet.write(index, i, heads[i])
    error_sheet.write(error_index, i+1, heads[i])
error_sheet.write(error_index, 10, "图像链接")
Beijing.save(r"Beijing.xls")
Error.save(r"Error.xls")

# 第一步，先把每个房子的链接拿到
for i in range(1):#int(len(district) / 2)):
    # 第一层循环，各个区域的链接
    dis_link = "http://www.ziroom.com/z/" + district[2 * i] + "/?isOpen=0"
    print()
    print(district[2 * i + 1], dis_link)
    dis_page = requests.get(dis_link, headers=headers)
    if dis_page.text:
        # 每个区域有多少页，直接在网页源码里面寻找"共x页"这个字符串
        page_num = re.search('共(\d+)页', dis_page.text, re.S).group(1)
        # 第二层循环，每一页的链接，每一页的链接就把根链接加上"-p"再加页码就可以了
        for j in range(1):#int(page_num)):
            print("\r第"+str(j+1)+"页，共"+page_num+"页", end='')
            sub_link = "http://www.ziroom.com/z/"+district[2 * i]+"-p"+str(j+1)+"/"
            try:
                sub_page = requests.get(sub_link, headers=headers, timeout=(3, 7))
            except:
                print("，超时，未获得")
            # 在每一页里面找房子的链接，规则就是www开头，html结尾
            # 这个规则是观察源代码得到的，所有的符合规则的代码存到link_box里面
            link_box = re.findall('www(.*?)html', sub_page.text)
            for k in range(len(link_box)):
                # print(link_box)
                # 把link_box print出来就知道下面为什么是这样了
                if link_box[2*k] == '.ziroom.com/about/lianxi.':
                    # 出现了这个联系自如，后面的就不用再看了，我也不知道后面的是哪来的房子。。浏览器上都没有显示的
                    break
                # 联系自如这个链接前面的，都是房源链接，因为刚好是重复的，所以跳着读
                # 这种方法可能会有重复，最后去重就可以了
                link_info = link_box[2*k]
                link = "http://www"+link_info+"html"
                # print(link)
                # 把链接和区域存到All_links里面去
                All_links.append([link, district[2 * i + 1]])
# 去重
for link in All_links:
    if link not in All_link:
        All_link.append(link)
print()
print("爬取完成，共"+str(len(All_links))+"条数据，去重以后还剩"+str(len(All_link))+"条")


# 这是读单张图片的函数
def read_this_page(link, index, error_index):
    attempts = 0
    success = False
    while attempts < 3 and not success:
        try:
            # 尝试三次。自如的网页有的时候会有404，用浏览器打开也有，没办法了。。
            # 超时也报错出去
            page = requests.get(link[0], headers=headers, timeout=(3, 7))

            # 价格
            price1 = re.search('Z_price(.*?)服务费另计', page.text, re.S).group(1)
            price2 = re.findall('background-position:(.*?)px', price1)
            price5 = "/"+re.search('<span>/(.*?)</span>', price1, re.S).group(1)
            price3 = []
            for w in range(len(price2)):
                price3.append(int(float(price2[w]) / -31.24))
            # print("价格矩阵：", price3)
            # 价格原图
            img_source = re.search('static(.*?)png', price1).group(1)
            img_link = "static" + img_source + "png"
            # print(img_link)
            # 有几个百度总是处理不好的，不如直接手动抄下来
            # 这个要是多了以后可以弄个字典，把所有的存起来
            if img_link == "static8.ziroom.com/phoenix/pc/images/2019/price/234a22e00c646d0a2c20eccde1bbb779.png":
                price_array = "1205837649"
            elif img_link == "static8.ziroom.com/phoenix/pc/images/2019/price/73ac03bb4d5857539790bde4d9301946.png":
                price_array = "7190864523"
            else:
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
                json_array = json1['words_result']
                price_array = json_array[0]['words']
            # print(price_array)
            # print(len(price_array))
            # 如果处理出来的长度是10，说明百度算对了，但是经常会出现1在首位，识别不到这个1。就报错
            if len(price_array) == 10:
                price4 = ''
                for n in range(len(price2)):
                    price4 = price4 + price_array[price3[n]]
            else:
                # 有报错的，后面也存到表格里面，价格标记成0，到时候再手动改一下
                price4 = '0'
                print()
                print("价格识别错误：", img_link)
                print("发生在这个房源：", link)

            # 小区
            village1 = re.search('Z_village_info(.*?)/h3', page.text, re.S).group(1)
            village2 = re.search('<h3>(.*?)<', village1, re.S).group(1)

            # 信息
            info = re.search('Z_home_b(.*?)tip-tempbox', page.text, re.S).group(1)
            info2 = re.findall('<dd>(.*?)</dd>', info, re.S)

            # 位置
            loc1 = re.search('Z_home_o(.*?)</li>', page.text, re.S).group(1)
            loc2 = re.search('<span class="ad">(.*?)</span>', loc1, re.S).group(1)

            # 输出，（有表格了就不需要输出了）
            # print("链接：", link[0])
            # print("价格： " + price4 + price5)
            # print("区域： " + link[1] + "区")
            # print("小区：", village2)
            # print("面积：", info2[0])
            # print("户型：", info2[2])
            # print("朝向：", info2[1])
            # print("位置：", loc2)
            print("读取完成", end='')
            info_to_write = [link[0], price4+price5, link[1]+"区", village2, info2[0], info2[2], info2[1], loc2]
            # 写到表格里面
            if price4 == '0':
                error_index = error_index + 1
                error_sheet.write(error_index, 0, "价格识别异常")
                error_sheet.write(error_index, 1, str(error_index))
                for i in range(len(info_to_write)):
                    error_sheet.write(error_index, 2+i, info_to_write[i])
                error_sheet.write(error_index, 10, img_link)
            else:
                index = index + 1
                sheet.write(index, 0, str(index))
                for i in range(len(info_to_write)):
                    sheet.write(index, 1+i, info_to_write[i])
            success = True
            if attempts != 0:
                print()
        except:
            # 尝试第二次和第三次
            attempts += 1
            if attempts == 1:
                print()
            print("\r房源链接解析异常:", link[0], end='， ')
            print("共3次尝试，现在是第" + str(attempts) + "次", end=' ')
            if attempts == 3:
                print("，链接解析失败")
                error_index = error_index + 1
                error_sheet.write(error_index, 0, "链接解析异常")
                error_sheet.write(error_index, 1, str(error_index))
                error_sheet.write(error_index, 2, link[0])
                break
    return index, error_index


# 这是主要的处理，主要是调用刚刚定义的那个函数
for link in All_link:
    print("\r第", index+error_index+1, "条", end='...     ')
    # 函数在这了
    index, error_index = read_this_page(link, index, error_index)
    if index % 100 == 0:
        print()
        print("已找到"+str(index)+"条数据")
        Beijing.save(r"Beijing.xls")
        Error.save(r"Error.xls")
    if error_index % 100 == 0 and error_index != 0:
        print()
        print("已找到" + str(error_index) + "条异常数据")
        Beijing.save(r"Beijing.xls")
        Error.save(r"Error.xls")
# 结束
print()
print("共找到"+str(index)+"条数据")
print("共找到" + str(error_index) + "条异常数据")
Beijing.save(r"Beijing.xls")
Error.save(r"Error.xls")
