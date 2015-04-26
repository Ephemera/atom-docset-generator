all: copy generate

.PHONY: all 

CURRENT_VER=$(shell curl -Is https://github.com/atom/atom/releases/latest | grep Location | awk -F '/' '{print $$NF}')

copy:
	rm -rf ./temp
	rm -rf ./Atom.docset/Contents/Resources/Documents/*
	httrack https://atom.io/docs/api/ -O ./temp +https://atom.io/docs/api/* +https://atom.io/assets/* -v
	mv ./temp/atom.io/docs/api/$(CURRENT_VER)/* ./Atom.docset/Contents/Resources/Documents/
	mv ./temp/atom.io/assets ./Atom.docset/Contents/Resources/Documents
	sed -i '' 's/\.\.\/\.\.\/\.\.\/assets/assets/' ./Atom.docset/Contents/Resources/Documents/*.html
	rm -rf ./temp

generate:
	python generator.py

compress:
	tar --exclude='.DS_Store' -cvzf Atom.tgz Atom.docset

