#!/usr/bin/env python3

import lxml.etree
import json
import os
import sys
import sqlite3

import beta_to_unicode

XML_PATH = "lexica/CTS_XML_TEI/perseus/pdllex/lat/ls/lat.ls.perseus-eng1.xml"

if len(sys.argv) > 1 and sys.argv[1] == "--android":
    DBNAME = "lewis-android.db"

    BOLD = '<b>'
    ITALIC = '<i>'
    UNBOLD = "</b>"
    UNITALIC = "</i>"
    NL = "<br/>"
    SPACE = '&nbsp;' * 2
else:
    DBNAME = "lewis.db"

    BOLD = "\033[1m"
    ITALIC = "\033[3m"
    UNBOLD = UNITALIC = "\033[0m"
    NL = '\n'
    SPACE = '  '

parser = lxml.etree.XMLParser(no_network=False)
root = lxml.etree.parse(XML_PATH, parser=parser)

betacode_replacer = beta_to_unicode.Replacer()

def xml2str(xml, level=0):
    if xml.tag == "sense":
        level = int(xml.get("level"))
    contents = (xml.text or '') + ''.join(xml2str(i, level) for i in xml)
    tail = xml.tail or ''

    if xml.tag == "orth":
        return BOLD + contents + UNBOLD + tail
    elif xml.tag == "gen":
        return ITALIC + contents + UNITALIC + tail
    elif xml.tag == "sense":
        return NL + level*SPACE + BOLD + xml.get('n') + ('. ' if xml.get('n')[-1] != ')' else ' ') + UNBOLD + contents.strip('— ') + tail
    elif xml.tag == "hi" and xml.get("rend") == "ital":
        return ITALIC + contents + UNITALIC + tail
    elif xml.tag == "foreign" and xml.get("lang") == "greek":
        return betacode_replacer.beta_code(contents.upper()) + tail
    elif xml.tag == "cit":
        if tail.endswith(': '):
            tail = tail.rstrip(': ')
        return NL + (level+1) * SPACE + contents + tail
    elif xml.tag == "quote":
        return '“' + contents + "”" + tail
    else:
        return contents + tail


def create_db(dictionary):
    if os.path.exists(DBNAME):
        os.remove(DBNAME)

    conn = sqlite3.connect(DBNAME)
    c = conn.cursor()
    c.execute("CREATE TABLE dictionary (_id INTEGER PRIMARY KEY, key TEXT, word TEXT, description TEXT)")
    c.executemany("INSERT INTO dictionary (key, word, description) VALUES (?, ?, ?)", dictionary)
    conn.commit()
    conn.close()

entries = root.findall("//entryFree")

dictionary = []
for i, entry in enumerate(entries):
    print(i, "/", len(entries), "\r", sep='', end='')

    key = entry.get("key").lower().strip("0123456789")
    key = key.replace('j', 'i').replace('v', 'u')

    word = entry[0].text.replace('-', '')

    assert entry.text is None # May as well assert instead of just assuming this
    value = ''.join(map(xml2str, entry)) + (entry.tail or '')
    value = value.replace(" ...", "…")
    value = value.replace("^", "") # XXX: Render proper diacritics: https://github.com/PerseusDL/lexica/issues/41

    dictionary.append((key, word, value))

print(len(entries), "/", len(entries), sep='')

create_db(dictionary)
