
install-libs:
	apt-get install python-pip
	pip install -U selenium nose

test:
	cd tests; nosetests
