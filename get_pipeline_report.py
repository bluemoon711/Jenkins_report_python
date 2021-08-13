#get the newest build result on the single pipeline
import sys
import requests
import json
import csv
import pandas as pd


if len(sys.argv) == 1:
    sys.exit(1)

pipeline_name = sys.argv[1]

base_url = 'http://jenkins..../job/'
api_req = '/job/....pipeline/wfapi/runs'
r = requests.get(base_url + pipeline_name + api_req)

json_data = r.json()
with open('data.json', 'w') as f:
    json.dump(json_data, f)
    
recent_build = json_data[0]

run_list = []
for stage in recent_build['stages']:
    detail = {}
    detail[stage['name']+'#'+stage['id']] = stage['status']
    run_list.append(detail)
#print(run_list)

fail_list = []
for run in run_list:
    newDict = dict(filter(lambda elem: elem[1] == 'FAILED', run.items()))
    if len(newDict) == 1:
        fail_list.append(newDict)
 #print(fail_list)

with open('pipe.csv', 'w') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerow([pipeline_name, recent_build['name']])
    for i in fail_list:
        for key, value in i.items():
            writer.writerow([key, value])

df = pd.read_csv('pipe.csv')
df.to_csv('report.csv', index = False)

