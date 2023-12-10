import requests

response = requests.get('https://javdb.com/actors/A0Qy?sort_type=0&t=74')

print(response.text)