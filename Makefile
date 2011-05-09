dist:
	rm -f MANIFEST
	python setup.py sdist

.PHONY: dist
