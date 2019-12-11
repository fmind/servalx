.PHONY: dist

SHELL := /bin/bash

dev: env;

env: clean_env
	tox -e venv

test:
	tox -e py27

docs:
	tox -e docs

setup:
	tox -e setup

coverage:
	tox -e coverage

all:
	tox

dist: clean
	venv/bin/python setup.py bdist_wheel

install: dist
	yes | pip uninstall servalx
	pip install --user dist/*.whl

clean_env:
	rm -rf venv

clean_tox:
	rm -rf .tox
	rm -rf .cache

clean_docs:
	rm -rf docs/html/
	rm -rf docs/apidoc/
	rm -rf docs/doctrees/

clean_build:
	rm -rf dist/
	rm -rf build/
	find . -name '*.egg' -exec rm -rf {} +
	find . -name '*.eggs' -exec rm -rf {} +
	find . -name '*.egg-info' -exec rm -rf {} +

clean_python:
	find . -name '*.pyc' -exec rm -rf {} +
	find . -name '*.pyo' -exec rm -rf {} +
	find . -name '*.pyd' -exec rm -rf {} +
	find . -name '__pycache__' -exec rm -rf {} +

clean: clean_build clean_python;

cleanall: clean clean_env clean_tox clean_docs;
