import sys
import requests
import json
import csv
import pandas as pd

if len(sys.argv) == 1:
	sys.exit(1)

pipeline_name = sys.argv[1]

base_url = 'http://jenkin..../job/'
api_req = '/job/....._pipeline/wfapi/runs'
r = requests.get(base_url + pipeline_name + api_req)

json_data = r.json()
with open('data.json', 'w') as f:
	json.dump(json_data, f)
#print(len(json_data))

run_list = []

for run in json_data:
	build = {}
	for stage in run['stages']:
		#print(run['name'] + "  " + stage['name'] +'#'+ stage['id'] + "  " + stage['status'])
		build[run['name'] + "  " + stage['name'] +'#'+ stage['id']] = stage['status']
	run_list.append(build)

fail_list = []
for run in run_list:
	newDict = dict(filter(lambda elem: elem[1] == 'FAILED', run.items()))
	if len(newDict) > 0:
		fail_list.append(newDict)
#print(fail_list)

with open('csvfile.csv', 'w') as f:
	writer = csv.writer(f, delimiter=',')
	for i in fail_list:
		for key, value in i.items():
			writer.writerow([key, value])
df = pd.read_csv('csvfile.csv')
df.to_csv(pipeline_name + '.csv', index = False)
