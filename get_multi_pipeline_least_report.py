import requests
import json
import csv
import pandas as pd

#get results of 3 different pipelines information together
names = ['pipeline1', 'pipeline2', 'pipeline3']
base_url = 'http://jenkin...pipelines/wfapi/runs'
for name in names: 
	r = requests.get(base_url + name + api_req)
	json_data = r.json()
	with open('data.json', 'w') as f:
		json.dump(json_data, f)
		recent_build = json_data[0]
		run_list = []
		for stage in recent_build['stages']:
			detail = {}
			detail[stage['name']+'#'+stage['id']] = stage['status']
			run_list.append(detail)
		fail_list = []
		for run in run_list:
			newDict = dict(filter(lambda elem: elem[1] == 'FAILED', run.items()))
			if len(newDict) == 1:
				fail_list.append(newDict)
	with open('pipe.csv', 'a') as f:
		writer = csv.writer(f, delimiter=',')
		writer.writerow([name, recent_build['name']])
		for i in fail_list:
			for key, value in i.items():
				writer.writerow([key, value])
		writer.writerow(['################################', '######'])
df = pd.read_csv('pipe.csv')
df.to_csv('report.csv', index = False)
