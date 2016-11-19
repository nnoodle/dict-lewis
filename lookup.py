import json
import sys

with open("lewis.json") as dicfile:
    dictionary = json.load(dicfile)

key = sys.argv[1].lower()
key = key.replace('j', 'i').replace('v', 'u')
definitions = dictionary[key]
print(*definitions, end='')
