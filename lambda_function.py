import json
import requests
from bs4 import BeautifulSoup
import datetime
import time
import os

KST = datetime.timezone(datetime.timedelta(hours=9))

def lambda_handler(event, context):
    WEBHOOK_URL = os.environ['INCOMING_WEBHOOK_URL']

    attachments = []  # for payloads. final result goes here
    
    # CODEFORCES
    cf_list = get_codeforces_contests()
    if not cf_list['fetch']:
        attachments.append({
            'color': '#FF0000',
            'fields': [{
                'value': 'error fetching codeforces'
            }]
        })
    else:
        print(cf_list)
        for x in cf_list['contests']:
            name = x['name']
            starts = datetime.datetime.fromtimestamp(x['startTimeSeconds'], KST).strftime('%Y-%m-%d %H:%M')
            ends = datetime.datetime.fromtimestamp(x['startTimeSeconds'] + x['durationSeconds'], KST).strftime('%Y-%m-%d %H:%M')
            url = f'https://codeforces.com/contests/{x["id"]}'
            
            attachments.append({
                'color': '#EF9AAF',
                'fields': [{
                    'title': name,
                    'value': f'{starts} ~ {ends} | {url}',
                    'short': False
                }]
            })
    # CODEFORCES END

    # ATCODER
    at_list = get_atcoder_contests()
    if not at_list['fetch']:
        attachments.append({
            'color': '#FF0000',
            'fields': [{
                'value': 'error fetching atcoder'
            }]
        })
    else:
        print(at_list)
        for x in at_list['contests']:
            name = x['name']
            starts = datetime.datetime.fromtimestamp(x['starts']).strftime('%Y-%m-%d %H:%M')
            ends = datetime.datetime.fromtimestamp(x['ends']).strftime('%Y-%m-%d %H:%M')
            url = x['url']
            
            attachments.append({
                'color': '#EF9AAF',
                'fields': [{
                    'title': name,
                    'value': f'{starts} ~ {ends} | {url}',
                    'short': False
                }]
            })
    # ATCODER END

    now = datetime.datetime.now(KST)
    nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
    payloads = {
        'text': f'{nowDatetime} 기준 콘테스트 목록',
        'attachments': attachments
    }

    req = requests.post(
        WEBHOOK_URL,
        data=json.dumps(payloads),
        headers={'Content-Type': 'application/json'}
    )

    if req.status_code != 200:
        return {
            'statusCode': 200,
            'body': json.dumps('failed')
        }
    else:
        return {
            'statusCode': 200,
            'body': json.dumps('succeed')
        }


def get_codeforces_contests():
    CF_API = 'https://codeforces.com/api/contest.list'

    ret = {}  # return dict

    req = requests.get(CF_API).json()  # convert to python dict

    if req['status'] != 'OK':
        ret['fetch'] = False
    else:
        ret['fetch'] = True

    res = req['result']
    before_contest_list = [x for x in res if x['phase'] == 'BEFORE' and x['type'] == 'CF']
    
    ret['contests'] = before_contest_list
    
    return ret


def get_atcoder_contests():
    ATCODER_URL = 'https://atcoder.jp'
    
    ret = {}  # return dict

    req = requests.get(ATCODER_URL + '/contests')
    if req.status_code != 200:
        ret['fetch'] = False
    else:
        ret['fetch'] = True

    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    contests = soup.select('#contest-table-upcoming > div > div > table > tbody > tr')
    # contests = soup.select('#contest-table-recent > div > div > table > tbody > tr')

    ret['contests'] = []

    for x in contests:
        starts_str = x.select_one('td:nth-child(1) > a').text
        starts = time.mktime(datetime.datetime.strptime(starts_str, '%Y-%m-%d %H:%M:%S%z').timetuple())
        name = x.select_one('td:nth-child(2) > a').text
        url = x.select_one('td:nth-child(2) > a').get('href')
        duration_str = x.select_one('td:nth-child(3)').text
        h, m = map(int, duration_str.split(':'))
        duration = h * 60 * 60 + m * 60
        ends = starts + duration
        
        print(starts, ends, duration)
        ret['contests'].append({
            'name': name,
            'starts': starts,
            'ends': ends,
            'duration': duration,
            'url': ATCODER_URL + url
        })
    
    return ret