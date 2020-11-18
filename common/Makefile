.PHONY: help

.DEFAULT: help
help:
	@echo "TODO"

clean: clean-build
	rm -rf venv

clean-build:
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info

setup: clean
	pip3 install -U -r requirements.txt

setup-dev: clean
	python -m venv venv
	./venv/bin/pip install -U pip setuptools wheel
	./venv/bin/pip install -U -r requirements.txt

install: clean
	pip3 install -U -r requirements.txt

check-types:
	echo "Checking types" && \
		mypy common tests

check-flake8:
	echo "Checking code style" && \
		flake8 common tests

check-lint:
	echo "Linting code" && \
		pylint -j 0 common tests

test:
	echo "Running tests" && \
		PYTHONPATH=$${PYTHONPATH:-.} pytest

check: check-types check-flake8 check-lint test

init-venv:
	. ./venv/bin/activate

run-pipeline: setup check
