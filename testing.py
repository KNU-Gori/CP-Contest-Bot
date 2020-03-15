import json
import requests

ret = {}

req = requests.get('https://codeforces.com/api/contest.list')
print(req.status_code)

req = req.json()  # convert to python dict
print(req['status'])

res = req['result']
before_contest_list = [x for x in res if x['phase'] == 'BEFORE' and x['type'] == 'CF']
print(before_contest_list)

