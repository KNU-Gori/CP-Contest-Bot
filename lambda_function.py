import json
from datetime import *
import time
import requests
import os
import codeforces, atcoder

KST = timezone(timedelta(hours=9))


def lambda_handler(event, context):
    WEBHOOK_URL = os.environ['INCOMING_WEBHOOK_URL']

    attachments = []  # for payloads. final result goes here

    now = datetime.now(KST)
    now_s = now.strftime('%Y-%m-%d %H:%M:%S')
    
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
            starts = datetime.fromtimestamp(x['startTimeSeconds'], KST)
            starts_s = starts.strftime('%Y-%m-%d %H:%M')
            ends = datetime.fromtimestamp(x['startTimeSeconds'] + x['durationSeconds'], KST)
            ends_s = ends.strftime('%Y-%m-%d %H:%M')
            url = f'https://codeforces.com/contests/{x["id"]}'

            starts_delta = starts - now
            attach_text = ''
            if starts_delta.days != 0:
                attach_text += f'{starts_delta.days}일 '
            attach_text += f'{starts_delta.seconds // 3600}시간 후에 시작해요!'

            attachments.append({
                'mrkdwn_in': ['text'],
                'color': '#FFBE5C',
                'title': name,
                'text': attach_text,
                'fields': [
                    {
                        'title': '시작 일시',
                        'value': starts_s,
                        'short': True
                    }, {
                        'title': '종료 일시',
                        'value': ends_s,
                        'short': True
                    }, {
                        'title': '대회 URL',
                        'value': url,
                        'short': False
                    }
                ]
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
            starts = datetime.fromtimestamp(x['starts'])
            starts_s = starts.strftime('%Y-%m-%d %H:%M')
            ends = datetime.fromtimestamp(x['ends'])
            ends_s = ends.strftime('%Y-%m-%d %H:%M')
            url = x['url']

            starts_delta = starts - now
            attach_text = ''
            if starts_delta.days != 0:
                attach_text += f'{starts_delta.days}일 '
            attach_text += f'{starts_delta.seconds // 3600}시간 후에 시작해요!'

            attachments.append({
                'mrkdwn_in': ['text'],
                'color': '#9d3757',
                'text': attach_text,
                'title': name,
                'fields': [
                    {
                        'title': '시작 일시',
                        'value': starts_s,
                        'short': True
                    }, {
                        'title': '종료 일시',
                        'value': ends_s,
                        'short': True
                    }, {
                        'title': '대회 URL',
                        'value': url,
                        'short': False
                    }
                ]
            })
    # ATCODER END

    # MAIN
    payloads = {
        'text': f'{now_s} 기준 콘테스트 목록',
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
    # MAIN END
