.PHONY: all prepare-dev venv lint test test-lf doc upload clean
SHELL=/bin/bash

VENV_NAME?=venv
VENV_BIN=$(shell pwd)/${VENV_NAME}/bin

PYTHON=${VENV_BIN}/python3

all:
	@echo "make test - Run tests during development"
	@echo "make doc - Make documentation"
	@echo "make clean - Get rid of scratch and byte files"

prepare-dev:
	apt install chromedriver

venv: $(VENV_NAME)/bin/activate
$(VENV_NAME)/bin/activate: setup.py
	test -d $(VENV_NAME) || virtualenv -p python3 $(VENV_NAME)
	${PYTHON} -m pip install -U pip setuptools
	${PYTHON} -m pip install -e .[suggestion,devel]
	touch $(VENV_NAME)/bin/activate

lint: venv
	${PYTHON} -m pylint webdriverwrapper

test: venv
	$(PYTHON) -m pytest -v tests
test-lf: venv
	$(PYTHON) -m pytest -v tests --lf

doc:
	cd docs; make html

upload: venv
	${PYTHON} setup.py register sdist upload

clean:
	find . -name '*.pyc' -exec rm --force {} +
	rm -rf $(VENV_NAME) *.eggs *.egg-info dist build docs/_build .mypy_cache .cache
