#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: loveNight

import json
import itertools
import urllib
import requests
import os
import re
import sys
import multiprocessing

str_table = {
    '_z2C$q': ':',
    '_z&e3B': '.',
    'AzdH3F': '/'
}

char_table = {
    'w': 'a',
    'k': 'b',
    'v': 'c',
    '1': 'd',
    'j': 'e',
    'u': 'f',
    '2': 'g',
    'i': 'h',
    't': 'i',
    '3': 'j',
    'h': 'k',
    's': 'l',
    '4': 'm',
    'g': 'n',
    '5': 'o',
    'r': 'p',
    'q': 'q',
    '6': 'r',
    'f': 's',
    'p': 't',
    '7': 'u',
    'e': 'v',
    'o': 'w',
    '8': '1',
    'd': '2',
    'n': '3',
    '9': '4',
    'c': '5',
    'm': '6',
    '0': '7',
    'b': '8',
    'l': '9',
    'a': '0'
}

# str 的translate方法需要用单个字符的十进制unicode编码作为key
# value 中的数字会被当成十进制unicode编码转换成字符
# 也可以直接用字符串作为value
char_table = {ord(key): ord(value) for key, value in char_table.items()}


# 解码图片URL
def decode(url):
    # 先替换字符串
    for key, value in str_table.items():
        url = url.replace(key, value)
    # 再替换剩下的字符
    return url.translate(char_table)


# 生成网址列表
def buildUrls(word):
    # word = urllib.parse(word.decode('gbk').encode('utf-8'))
    url = r"http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&fp=result&queryWord={word}&cl=2&lm=-1&ie=utf-8&oe=utf-8&st=-1&ic=0&word={word}&face=0&istype=2nc=1&pn={pn}&rn=60"
    urls = (url.format(word=word, pn=x) for x in itertools.count(start=0, step=60))
    return urls


# 解析JSON获取图片URL
re_url = re.compile(r'"objURL":"(.*?)"')


# re_url = re.compile(r'"objURL":".*/(.*?)"')
# re_url = re.compile(r'.*/(.*?)\.jpg',re.S)
def resolveImgUrl(html):
    imgUrls = [decode(x) for x in re_url.findall(html)]
    return imgUrls


def downImg(imgUrl, dirpath, imgName):
    filename = os.path.join(dirpath, imgName)
    try:
        res = requests.get(imgUrl, timeout=15)
        if str(res.status_code)[0] == "4":
            print(str(res.status_code), ":", imgUrl)
            return False
    except Exception as e:
        print("raise exception", imgUrl)
        print(e)
        return False
    print(imgUrl)
    with open(filename, "wb") as f:
        f.write(res.content)
    return True


def mkDir(dirName):
    dirpath = os.path.join(sys.path[0], dirName)
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    return dirpath


def download_keyword(keyword, savepath, downloadnum):
    if not os.path.exists(savepath):
        os.makedirs(savepath)
    urls = buildUrls(keyword)
    index = 0

    for url in urls:
        print("Requesting: ", url)
        html = requests.get(url, timeout=10).content.decode('utf-8')
        imgUrls = resolveImgUrl(html)
        if len(imgUrls) == 0:
            break
        for url in imgUrls:
            name = keyword+'_'+str(index) + '.jpg'
            if downImg(url, savepath, name):
                index += 1
                print("keyword:{} downloaded at {}".format(keyword, index))

            if index > downloadnum:
                return
    print(keyword, ' suceess download!')
    print('system end')


def read_keywords(key_txt):
    keys = []
    with open(key_txt, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            keys.append(line.strip())
    return keys


if __name__ == '__main__':
    key_txt = './keywords.txt'
    keywords = read_keywords(key_txt)
    print("total:", keywords.__len__())

    downloadnum = 700
    for idx, k in enumerate(keywords):
        print(k)
        download_path = './data/' + k + '/'
        t = multiprocessing.Process(target=download_keyword, args=(k, download_path, downloadnum))
        t.start()
        # t.join()
        # download_keyword(k, download_path, downloadnum)

