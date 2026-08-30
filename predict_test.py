import requests, json

base='http://127.0.0.1:5000'

login = requests.post(base+'/api/auth/login', json={'username':'tester','password':'tester'}).json()
print('LOGIN RESPONSE:', json.dumps(login, indent=2))

token = login.get('token')
headers = {'Authorization': f'Bearer {token}'}

with open('ml_pipeline/results/pipeline_results.json') as f:
    features = json.load(f)['feature_names']

sample = {f:0 for f in features}

resp = requests.post(base+'/api/predict', json=sample, headers=headers)
print('\nPREDICT STATUS:', resp.status_code)
print('PREDICT RESPONSE:', json.dumps(resp.json(), indent=2))
