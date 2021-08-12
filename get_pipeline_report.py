import sys
import requests
import json
import csv
import pandas as pd


if len(sys.argv) == 1:
    sys.exit(1)

pipeline_name = sys.argv[1]

base_url = 'http://jenkins-tt.drivecaminc.loc:8080/job/master/job/pipelines/job/cicd/job/'
api_req = '/job/00_master_pipeline/wfapi/runs'
r = requests.get(base_url + pipeline_name + api_req)

json_data = r.json()
with open('data.json', 'w') as f:
    json.dump(json_data, f)
#print (len(json_data))
#print(json_data[0])
recent_build = json_data[0]
#print(recent_build['name'])
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

#run_list = []
# for run in json_data:
#     print(run)
    # build = {}
    # for stage in run['stages']:
    #     #print (stage['name'] + "  " + stage['status'])
    #     build[stage['name']] = stage['status']
    # run_list.append(build)

# sns = []
# for element in run_list:
#     for key, value in element.items():
#         sns.append(key)
# set_sns = set(sns)
# #print (set_sns)

# with open('pipe.csv', mode='w') as csv_file:
#     fieldnames = set_sns
#     writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
#     writer.writeheader()
#     for r in run_list:
#         writer.writerow(r)

# with open('pipe.csv') as infile, open('report.csv', 'w') as outfile:
#     for line in infile:
#         if not line.strip(): continue  # skip the empty line
#         outfile.write(line)
