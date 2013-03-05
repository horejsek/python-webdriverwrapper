
PYTHON=`which python`


test:
	cd tests; nosetests --nologcapture


source:
	$(PYTHON) setup.py sdist

upload:
	$(PYTHON) setup.py register sdist upload

install:
	$(PYTHON) setup.py install

clean:
	$(PYTHON) setup.py clean
	rm -rf build/ MANIFEST
	find . -name '*.pyc' -delete


install-libs:
	apt-get install python-pip
	pip install -U selenium nose

install-building-packages:
	apt-get install build-essential dh-make debhelper devscripts
	pip install -U setuptools
