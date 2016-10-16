import json
import sys

with open("lewis.json") as dicfile:
    dictionary = json.load(dicfile)

definitions = dictionary[sys.argv[1].lower()]
print(*definitions, end='')
