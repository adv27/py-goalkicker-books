import io
import os
import shutil
from multiprocessing.dummy import Pool as ThreadPool

import requests
from bs4 import BeautifulSoup

AUTHOR = 'Vu Dinh Anh'

BOOKS_URL = r'http://goalkicker.com/#c4w26313y2t2y27444232374z28433'
BASE_URL = r'http://goalkicker.com'
DEFAULT_PATH = 'goalkicker_books'


def download_book(url: str):
    print('Downloading at: ' + url)
    subject = url.split('/')[-2]
    local_filename = url.split('/')[-1]

    cwd = os.getcwd()  # current working directory
    # create folder to saved book in
    parent_folder = cwd + '\\' + DEFAULT_PATH + '\\' + subject
    if not os.path.exists(parent_folder):
        os.makedirs(parent_folder)
    path_to_save = cwd + '\\' + DEFAULT_PATH + '\\' + subject + '\\' + local_filename

    # saving
    r = requests.get(url, stream=True)
    with io.open(path_to_save, 'wb') as file:
        shutil.copyfileobj(r.raw, file)

    print('Downloaded: ' + local_filename)


def new_download(url: str):
    _url = BASE_URL + '/' + url
    r = requests.get(_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    _url += '/' + soup.find('button', {'class': 'download'})['onclick'].split("'")[1]
    subject = _url.split('/')[-2]
    local_filename = _url.split('/')[-1]

    cwd = os.getcwd()  # current working directory
    # create folder to saved book in
    parent_folder = cwd + '\\' + DEFAULT_PATH + '\\' + subject
    if not os.path.exists(parent_folder):
        os.makedirs(parent_folder)
    path_to_save = cwd + '\\' + DEFAULT_PATH + '\\' + subject + '\\' + local_filename

    # saving
    print('Downloading at: ' + _url)
    r = requests.get(_url, stream=True)
    with io.open(path_to_save, 'wb') as file:
        shutil.copyfileobj(r.raw, file)

    print('Downloaded: ' + local_filename)


def get_urls() -> []:
    r = requests.get(BOOKS_URL)
    soup = BeautifulSoup(r.text, 'html.parser')
    anchors = soup.find_all('a', {'target': '_blank'})
    urls = {a['href']: '' for a in anchors}
    for index, url in enumerate(urls, 1):
        _url = BASE_URL + '/' + url
        r = requests.get(_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        urls[url] = soup.find('button', {'class': 'download'})['onclick'].split("'")[1]
        print('%s - Book: %-30s file_name: %s' % (index, url, urls[url]))
    return urls


def foo():
    r = requests.get(BOOKS_URL)
    soup = BeautifulSoup(r.text, 'html.parser')
    # urls = []
    anchors = soup.find_all('a', {'target': '_blank'})
    # for a in anchors:
    #     urls.append(a['href'])
    urls = list(map(lambda a: a['href'], anchors))
    pool = ThreadPool(15)
    results = pool.map(new_download, urls)
    pool.close()
    pool.join()


def main():
    # book_urls_dict = get_urls()
    # for url in book_urls_dict:
    #     _url = BASE_URL + '/' + url + '/' + book_urls_dict[url]
    #     download_book(_url)
    foo()


if __name__ == '__main__':
    main()
