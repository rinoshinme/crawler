import sys
import traceback
import urllib.error

import pandas as pd
import os
import sys
sys.path.append('./')

import time

ticks = time.time()


def urllib_download(url, name):
    from urllib.request import urlretrieve
    urlretrieve(url, name)
    
"""
使用前需根据爬取数据的表格修改72、77行的大图跳转地址及关键词列号
"""


dir = "./xlsx/"
pass_dir = "./xlsx_downloaded/"
pic_dir = "./images/"

if not os.path.exists(pass_dir):
    os.mkdir(pass_dir)

if not os.path.exists(pic_dir):
    os.mkdir(pic_dir)

file_list = os.listdir(dir)
file_list.sort()
file_total_num = len(file_list)
file_num = 0

from lxml import etree

from selenium import webdriver


def urllib_download(url, name):
    from urllib.request import urlretrieve
    urlretrieve(url, name)


option = webdriver.ChromeOptions()
option.add_argument("blink-settings=imagesEnabled=false")  # 不加载图片

driver = webdriver.Chrome(options=option)
print(file_list)

for file in file_list:
    print(file)

    df = pd.read_excel(dir + file)

    print(df.columns)
    print(df.describe())

    t1 = time.time()

    total = len(df.index)

    old_src = ''
    idx = 0

    for indexs in df.index:
        try:
            if indexs == 0:
                old_src = df.loc[indexs].values[1]
            img_url = df.loc[indexs].values[1] #  大图跳转地址列号
            print("img_url", img_url)

            driver.get(img_url)

            src = df.loc[indexs].values[4]  # 搜索关键词列号

            if old_src != src:
                idx = 0
            idx += 1
            selector = etree.HTML(driver.page_source)

            img_src = selector.xpath("//*[@id='mainImageWindow']/div[1]/div/div/div/img/@src")[0]

            new_name = pic_dir + src + '_' + (str(idx)).zfill(4) + ".jpg"
            print(img_src, src + ' ' + str(indexs) + '/' + str(total) + ', file:',
                  str(file_num) + '/' + str(file_total_num))
            print(new_name)
            old_src = src
            try:
                urllib_download(img_src, new_name)
            except urllib.error.HTTPError as err:
                print("HttpError:", err)
                traceback.print_exc()
                urllib_download(img_url, new_name)
        except urllib.error.HTTPError as err:
            print("HttpError:", err)
            traceback.print_exc()

            continue
        except:
            print("Unexpected error:", sys.exc_info()[0])
            traceback.print_exc()
            continue
    file_num += 1
