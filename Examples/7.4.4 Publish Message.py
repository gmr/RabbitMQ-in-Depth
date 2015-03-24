import requests

payload = {'body': 'from statelessd', 'app_id': 'example'}
response = requests.post('http://localhost:8900/%2f/amq.topic/example',
                         auth=('guest', 'guest'),
                         data=payload)
