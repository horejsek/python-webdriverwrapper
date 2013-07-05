
PYTHON=`which python`
PYTHON3=`which python3`


test:
	cd tests; $(PYTHON) alltests.py
	cd tests; $(PYTHON3) alltests.py

source:
	$(PYTHON) setup.py sdist

upload:
	$(PYTHON) setup.py register sdist upload

install:
	$(PYTHON) setup.py install
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
