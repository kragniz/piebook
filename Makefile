SETUP=python setup.py
all:
	$(SETUP) build

install:
	$(SETUP) install

dist:
	$(SETUP) sdist

notes:
	find -name \*.py | xargs grep -nH -E 'TODO|FIXME'


.PHONY: all install dist notes
