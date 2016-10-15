import json
import sys

with open("lewis.json") as dicfile:
    dictionary = json.load(dicfile)

for definition in dictionary[sys.argv[1].lower()]:
    print(definition)
