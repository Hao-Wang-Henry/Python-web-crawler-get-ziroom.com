import requests
import re

# 配置浏览器
# 这个要在你自己的浏览器里面查
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

# 第一步，先把每个房子的链接拿到
for i in range(int(len(district) / 2)):
    # 第一层循环，各个区域的链接
    dis_link = "http://www.ziroom.com/z/" + district[2 * i] + "/?isOpen=0"
    print()
    print(district[2 * i + 1], dis_link)
    dis_page = requests.get(dis_link, headers=headers)
    if dis_page.text:
        # 每个区域有多少页，直接在网页源码里面寻找"共x页"这个字符串
        page_num = re.search('共(\d+)页', dis_page.text, re.S).group(1)
        # 第二层循环，每一页的链接，每一页的链接就把根链接加上"-p"再加页码就可以了
        for j in range(int(page_num)):
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
