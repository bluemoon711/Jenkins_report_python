import sys
import requests
import json
import csv
import pandas as pd

if len(sys.argv) == 1:
    sys.exit(1)

job_name = sys.argv[1]
bld_num = sys.argv[2]
#this is used for master pipleline. Need to change the base for other pipelines
base = 'http://jenkins-tt.drivecaminc.loc:8080/job/master/job/pipelines/job/cicd/job/master/job/'
api_req = '/wfapi/describe'
r = requests.get(base + job_name + '/' + bld_num + api_req)

json_data = r.json()
with open('data.json', 'w') as f:
    json.dump(json_data, f)
#print(len(json_data))

run_list = []
stages = json_data.get('stages')
for stage in stages:
    detail = {}
    detail[stage['name']] = stage['status']
    run_list.append(detail)
#print(run_list)

fail_list = []
for run in run_list:
    newDict = dict(filter(lambda elem: elem[1] == 'FAILED', run.items()))
    if len(newDict) == 1:
        fail_list.append(newDict)
#print(fail_list)

with open('csvfile.csv', 'w') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerow([job_name, bld_num])
    for i in fail_list:
        for key, value in i.items():
            writer.writerow([key, value])

df = pd.read_csv('csvfile.csv')
df.to_csv(job_name + '_'+ bld_num +'.csv', index = False)