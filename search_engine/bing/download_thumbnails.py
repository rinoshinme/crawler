import sys
import traceback
import urllib.error

import pandas as pd
import os

import time

ticks = time.time()


def urllib_download(url, name):
    from urllib.request import urlretrieve
    urlretrieve(url, name)

"""
使用前需根据爬取数据的表格修改49、50行的缩略图地址及关键词列号
"""


dir = "./xlsx/"  # 未下图片的表格
pass_dir = "./xlsx_downloaded/"  # 已下载图片的表格存放路径，方便程序终止后不重复爬取
pic_dir = "./images/"  # 存储图片的目录

if not os.path.exists(pass_dir):
    os.mkdir(pass_dir)

if not os.path.exists(pic_dir):
    os.mkdir(pic_dir)

file_list = os.listdir(dir)
file_list.sort()
file_total_num = len(file_list)
file_num = 0

for file in file_list:

    df = pd.read_excel(dir + file)

    print(df.columns)
    print(df.describe())

    t1 = time.time()

    total = len(df.index)

    for indexs in df.index:
        try:
            img_url = df.loc[indexs].values[0]  # 缩略图地址的列号
            src = file.split('-')[7]  # 搜索关键词的列号

            new_name = pic_dir + src + '_' + (str(indexs)).zfill(4) + ".jpg"
            print(img_url, src + ' ' + str(indexs) + '/' + str(total) + ', file:',
                  str(file_num) + '/' + str(file_total_num))
            try:
                urllib_download(img_url, new_name)
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
    os.rename(dir + file, pass_dir + file)
