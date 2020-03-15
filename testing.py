import json
import requests
from bs4 import BeautifulSoup
import datetime
import time

ret = {}

req = requests.get('https://atcoder.jp/contests')
print(req.status_code)

html = req.text

soup = BeautifulSoup(html, 'html.parser')

contests = soup.select('#contest-table-upcoming > div > div > table > tbody > tr')
contests = soup.select('#contest-table-recent > div > div > table > tbody > tr')

ret = {}

for x in contests:
    starts_str = x.select_one('td:nth-child(1) > a').text
    starts = time.mktime(datetime.datetime.strptime(starts_str, '%Y-%m-%d %H:%M:%S%z').timetuple())
    name = x.select_one('td:nth-child(2) > a').text
    url = x.select_one('td:nth-child(2) > a').get('href')
    duration_str = x.select_one('td:nth-child(3)').text
    h, m = map(int, duration_str.split(':'))
    duration = h * 60 * 60 + m * 60
    ends = starts + duration
    
    print(url)