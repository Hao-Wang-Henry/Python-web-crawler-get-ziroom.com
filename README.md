
# Python-web-crawler-get-ziroom.com

## request.py是整体的程序
19-20行需要把AK和SK改成自己的
26-29行需要把浏览器的配置改成自己的

## request2.py的处理方式跟request.py一样
区别在于request2没有循环，只是把东城区第一页的29个房子爬下来了

## get_page,py就是整体程序的第一步，获取每一个链接
但是获取下来以后我没有存，你可以自己print
6-9行需要把浏览器的配置改成自己的

## get_page.py是从每一页获取信息并print出来
（没有解析价格）

## number_identify.py是识别图像的程序，可以随意指定一个图像识别
15-16行改成你自己的AK和SK
如果是网图，就把23行的链接改掉
如果是本地图，就把23-31行注释掉，然后在32行换上你自己的地址
