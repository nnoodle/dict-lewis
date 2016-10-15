import lxml.etree
import json

RESET = "\033[0m"
BOLD = "\033[1m"
ITALIC = "\033[3m"

parser = lxml.etree.XMLParser(no_network=False)
root = lxml.etree.parse("lat.ls.perseus-eng1.xml", parser=parser)

def xml2str(xml):
    contents = (xml.text or '') + ''.join(map(xml2str, xml))
    tail = xml.tail or ''

    if xml.tag == "orth":
        return BOLD + contents + RESET + tail
    elif xml.tag == "gen":
        return ITALIC + contents + RESET + tail
    elif xml.tag == "sense":
        return '\n' + int(xml.get("level"))*'  ' + BOLD + xml.get('n') + '.' + RESET + contents + tail
    elif xml.tag == "hi" and xml.get("rend") == "ital":
        return ITALIC + contents + RESET + tail
    else:
        return contents + tail


dictionary = {}
for entry in root.iterfind("//entryFree"):
    key = entry.get("key").lower().strip("0123456789")

    assert entry.text is None # May as well assert instead of just assuming this
    value = ''.join(map(xml2str, entry)) + (entry.tail or '')

    if key in dictionary:
        dictionary[key].append(value)
    else:
        dictionary[key] = [value]

with open("lewis.json", 'w') as dicfile:
    json.dump(dictionary, dicfile)
