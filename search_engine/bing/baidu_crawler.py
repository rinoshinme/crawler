import time
import requests
import json
#进行UA伪装
header = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}
url = 'https://image.baidu.com/search/acjson?'
#将编码形式转换为utf-8
# pn是从第几张图片获取 百度图片下滑时默认一次性显示30张
pn=1
n=1
prefix='cqgm' #图片名前缀
save_path=r'D:\atmp\city\2/' #文件保存路径
#修改param里面的queryword 以及word 为搜索关键词
for m in range(1, 350): #m为页数，最后爬取图片数为m*rn rn=30,注意一般也只能爬到2000张左右
    url = 'https://image.baidu.com/search/acjson?'
    #param 其他元素不修改应该也可以用 ，如果有问题看下文如何修改
    param = {
        'tn': 'resultjson_com',
        'logid':'10303476195752336246',
        'ipn': 'rj',
        'ct': '201326592',
        'is':'',
        'fp': 'result',
        'fr':'',
        'word': '占道经营',
        'queryWord': '占道经营',
        'cl': '2',
        'lm': '-1',
        'ie': 'utf-8',
        'oe': 'utf-8',
        'adpicid':'',
        'st': '-1',
        'z':'',
        'ic':'',
        'hd':'',
        'latest':'',
        'copyright':'',
        's':'',
        'se':'',
        'tab':'',
        'width':'',
        'height':'',
        'face': '0',
        'istype': '2',
        'qc':'',
        'nc': '1',
        'expermode':'',
        'nojc':'',
        'isAsync':'',
        'pn': pn,
        'rn': '30',
        'gsm': 'b4',
        '1650873660735':''
    }
    page_text = requests.get(url=url, headers=header, params=param)
    page_text.encoding = 'utf-8'
    try:
        page_text = page_text.json()
    except:
        pn+=1
        continue
    info_list = page_text['data']
    del info_list[-1]
    img_path_list = []
    for i in info_list:
        img_path_list.append(i['thumbURL'])

    for img_path in img_path_list:
        img_data = requests.get(url=img_path, headers=header).content
        time.sleep(0.5)

        img_path = save_path + prefix+str(n).zfill(6) + '.jpg'
        with open(img_path, 'wb') as fp:
            fp.write(img_data)
        n = n + 1 
    time.sleep(5) #增加睡眠时间避免被屏蔽
    pn += 29