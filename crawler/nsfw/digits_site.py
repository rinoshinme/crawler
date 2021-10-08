"""
2345678av.com
"""

import requests
from bs4 import BeautifulSoup
import os
from urllib import request
import time
from .base import HEADERS


CATEGORY_MAP = {
    'base': 'list-39-2120-{}.html'
}


class DigitsSite(object):
    CATEGORIES = []

    def __init__(self, category):
        self.category = category
        self.page_suffix = CATEGORY_MAP[self.category]
        self.homepage = 'https://www.2345678av.com/'
        self.res_encoding = 'GB2312'
    
    def get_page_url(self, page_index):
        page_url = '{}{}'.format(self.homepage, self.page_suffix.format(page_index))
        return page_url
    
    def get_page_info(self, page_url):
        data = []
        try:
            response = requests.get(page_url, headers=HEADERS)
            response.encoding = self.res_encoding
            soup = BeautifulSoup(response.text, features='lxml')
            container = soup.find(attrs={'class', 'appel'})
            items = container.find_all('li')
            for item in items:
                try:
                    title = item.a.text
                    url = item.a['href']
                    url = self.homepage + url
                    data.append({
                        'url': url, 
                        'title': title
                    })
                except Exception as ee:
                    print('error: ' + str(ee))
                    
        except Exception as e:
            print('error: ' + str(e))
        
        return data
    
    def get_set_info(self, set_url):
        image_urls = []
        try:
            response = requests.get(set_url, headers=HEADERS)
            response.encoding = self.res_encoding
            soup = BeautifulSoup(response.text, features='lxml')
            container = soup.find(attrs={'class': 'ttnr'})

            for d in container.find_all('img'):
                image_urls.append(d['src'])

        except Exception as e:
            print('error: ' + str(e))
        
        return image_urls
    
    def download_image(self, image_url, image_path):
        try:
            req = request.Request(image_url, headers=HEADERS)
            data = request.urlopen(req).read()
            if len(data) > 0:
                with open(image_path, 'wb') as f:
                    f.write(data)
        except Exception as e:
            print('download error: ' + str(e))
            return
    
    def title_simplify(self, title):
        title = title.replace('?', '').replace(':', '').replace('|', '')
        return title

    def run(self, save_root, start=1, end=-1):
        current = start
        while True:
            print('[Page] {}'.format(current))
            page_url = self.get_page_url(current)
            set_data = self.get_page_info(page_url)
            # print(set_data)

            for info in set_data:
                set_url = info['url']
                title = info['title']
                title = self.title_simplify(title)
                print('[Set] {}'.format(title))
                image_urls = self.get_set_info(set_url)
                for imgurl in image_urls:
                    save_name = os.path.basename(imgurl)
                    save_folder = os.path.join(save_root, title)
                    if not os.path.exists(save_folder):
                        os.makedirs(save_folder)
                    save_path = os.path.join(save_folder, save_name)
                    if not os.path.exists(save_path):
                        print('[Image] {}'.format(imgurl))
                        self.download_image(imgurl, save_path)
                        time.sleep(0.1)

            current += 1
            if end > 0 and current > end:
                break
