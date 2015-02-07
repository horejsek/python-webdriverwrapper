
PYTHON=`which python`
PYTHON3=`which python3`


test:
	cd tests; py.test `find -iname "*.py"`
test-lastfail:
	cd tests; py.test --lf `find -iname "*.py"`

doc:
	cd docs; make html

source:
	$(PYTHON) setup.py sdist

upload:
	$(PYTHON) setup.py register sdist upload

install:
	@echo "Instaling for Python 2..."
	$(PYTHON) setup.py install
	@echo "Instaling for Python 3..."
	$(PYTHON3) setup.py install

clean:
	$(PYTHON) setup.py clean
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
