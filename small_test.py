import requests
from bs4 import BeautifulSoup

BOOKS_URL = r'http://goalkicker.com/#c4w26313y2t2y27444232374z28433'

r = requests.get(BOOKS_URL)
# r.text để lấy được code HTML của trang web đang đc request tới
soup = BeautifulSoup(r.text, 'html.parser') # BeautifulSoup đc sử dụng để lọc HTML
anchors = soup.find_all('a', {'target': '_blank'}) # lấy toàn bộ thẻ a trong trang web
for a in anchors:
    print('{} {}'.format(a, a['href']))  # lấy và in ra thuộc tính 'href' từ thẻ a
