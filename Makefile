dist:
	$(RM) MANIFEST
	python setup.py sdist

clean:
	$(RM) MANIFEST
	find -type f -name '*.pyc' -delete

.PHONY: dist clean
