import requests
import json

iss_now = requests.get("http://api.open-notify.org/iss-now.json")

data = iss_now.content
load =  json.loads(data)

print(load)
print(load["timestamp"])
