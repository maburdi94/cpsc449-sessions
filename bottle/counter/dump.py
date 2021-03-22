
import sys
import requests

# sys.argv[1]
url = sys.argv[1]

r = requests.get(url).json()

keys = r['keys']

for key in keys:
    r = requests.get(f'{url}/{key}')
    print(r.text)
