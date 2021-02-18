#!/usr/bin/env python3

import os
import sys
import lxml.etree
from datetime import datetime

import beta_to_unicode

XML_PATH = "lexica/CTS_XML_TEI/perseus/pdllex/lat/ls/lat.ls.perseus-eng1.xml"
LAT_GRK = dict(zip("abgdez", "αβγδεζ"))

DBNAME = "lewis.txt"
BOLD = '{'
UNBOLD = '}'
ITALIC = ''
UNITALIC = ''
NL = '\n'
SPACE = '   '

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
        n = xml.get('n')
        if level == 5:
            n = ''.join(LAT_GRK[i] if i.isalpha() else i for i in n)
        n += '. ' if n[-1] != ')' else ' '
        return NL + level*SPACE + BOLD + n + UNBOLD + contents.strip('— ') + tail
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

with open(DBNAME, mode='w', encoding='utf-8') as file:
    print("Reading from " + XML_PATH)

    file.write('Text provided under a CC BY-SA license by Perseus Digital Library, http://www.perseus.tufts.edu, with funding from The National Endowment for the Humanities.'+
               f'Data accessed from https://github.com/PerseusDL/lexica/ [{datetime.now().isoformat()}].\n\n')

    context = lxml.etree.iterparse(XML_PATH, no_network=False, events=("end",), tag="entryFree")
    for i, (_, entry) in enumerate(context):
        print("\rProcessing entry ", i, sep='', end='')

        key = entry.get("key").lower().strip("0123456789")
        key = key.replace('j', 'i').replace('v', 'u')

        assert entry[0].tag == "orth"
        word = entry[0].text.replace('-', '')

        assert entry.text is None # May as well assert instead of just assuming this
        value = ''.join(map(xml2str, entry)) + (entry.tail or '')
        value = value.replace(" ...", "…")

        # XXX: Render proper diacritics: https://github.com/PerseusDL/lexica/issues/41
        word = word.replace("^", "")
        value = value.replace("^", "")

        file.write(f':{key if key == word else key+"¦"+word}: {value}') # key+'\n'+word+'\n'+value+'\n'
        entry.clear()
        print()

print("Finished generating " + DBNAME)
