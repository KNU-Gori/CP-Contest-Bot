import json
import datetime
import time
import requests
import os
import codeforces, atcoder

KST = datetime.timezone(datetime.timedelta(hours=9))


def lambda_handler(event, context):
    WEBHOOK_URL = os.environ['INCOMING_WEBHOOK_URL']

    attachments = []  # for payloads. final result goes here
    today_cnt = 0  # num of contests which start today
    
    # CODEFORCES
    cf_list = codeforces.get_contests()
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
                'color': '#FFBE5C',
                'fields': [{
                    'title': name,
                    'value': f'{starts} ~ {ends} | {url}',
                    'short': False
                }]
            })
    # CODEFORCES END

    # ATCODER
    at_list = atcoder.get_contests()
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
                'color': '#9d3757',
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
