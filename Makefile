
PYTHON2=`which python2`
PYTHON3=`which python3`


test:
	$(PYTHON2) -m pytest -v tests
	$(PYTHON3) -m pytest -v tests
test-lastfail:
	$(PYTHON3) -m pytest -v --lf tests

doc:
	cd docs; make html

source:
	$(PYTHON2) setup.py sdist

upload:
	$(PYTHON2) setup.py register sdist upload

install:
	@echo "Instaling for Python 2..."
	$(PYTHON2) setup.py install
	@echo "Instaling for Python 3..."
	$(PYTHON3) setup.py install

clean:
	$(PYTHON2) setup.py clean
	rm -rf build/ MANIFEST
	find . -name '*.pyc' -delete


install-libs:
	apt-get install python-pip
	pip-2.7 install -U selenium nose
	pip-3.2 install -U selenium nose

install-building-packages:
	apt-get install build-essential dh-make debhelper devscripts
	pip-2.7 install -U setuptools
	pip-3.2 install -U setuptools
