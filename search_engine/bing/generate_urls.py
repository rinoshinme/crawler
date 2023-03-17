# import pandas as pd

def load_words(text_path):
    key_words = []
    with open(text_path, 'r') as f:
        for line in f.readlines():
            key_words.append(line.strip())
    return key_words


def generate_urls(keywords_path):
    words = load_words(keywords_path)
    urls = []
    for word in words:
        url = "https://www.bing.com/images/search?q="+ word +"&form=HDRSC2&first=1&tsc=ImageBasicHover"
        urls.append(url)
    return urls


if __name__ == '__main__':
    urls = generate_urls('./key_words.txt')
    for url in urls:
        print(url)
