#!/usr/bin/env python3

import json
import os
import sys
import sqlite3

with open("lewis.json") as dicfile:
    dictionary = json.load(dicfile)

try:
    os.remove("lewis.db")
except:
    pass

entries = [(word, desc) for word, v in dictionary.items() for desc in v]

conn = sqlite3.connect("lewis.db")
c = conn.cursor()
c.execute("CREATE TABLE dictionary (word text, description text)")
c.executemany("INSERT INTO dictionary VALUES (?,?)", entries)
conn.close()
