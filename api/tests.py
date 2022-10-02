import requests
import json

payload = {"name": "sabino", "size": "huge"}
r = requests.post("http://localhost:8000/predict", data=json.dumps(payload))
print(r.json())
