URL = 'https://github.com/PerseusDL/lexica'
NAME = 'Charlton T. Lewis, Charles Short, A Latin Dictionary'

PREFIX = /usr

lewis.dict.dz: lewis.dict
	dictzip lewis.dict

lewis.txt: extract.py
	./extract.py

lewis.dict lewis.index: lewis.txt
	dictfmt --utf8 --allchars -u $(URL) -s $(NAME) --columns 80 -j lewis --headword-separator '¦' < lewis.txt

install:
	install -m 0755 -d "${PREFIX}/share/dictd"
	install -m 0644 -t "${PREFIX}/share/dictd/" lewis.dict.dz lewis.index

uninstall:
	rm -f "${PREFIX}/share/dictd/lewis.dict.dz" "${PREFIX}/share/dictd/lewis.index"

clean:
	rm -f lewis.txt lewis.dict lewis.dict.dz lewis.index
