all: copy generate

.PHONY: all 

copy:
	rm -rf ./temp
	rm -rf ./Atom.docset/Contents/Resources/Documents
	httrack https://atom.io/docs/api/ -O ./temp +https://atom.io/docs/api/* -v
	mv "$$(find temp/atom.io/docs/api -type d | tail -n 1)" ./Atom.docset/Contents/Resources/Documents
	rm -rf ./temp

generate:
	python generator.py

compress:
	tar --exclude='.DS_Store' -cvzf Atom.tgz Atom.docset

