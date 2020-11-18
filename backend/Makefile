.PHONY: help

.DEFAULT: help
help:
	@echo "TODO"

CONDA_ENV=cee-hacks-2020-images-backend

# creates environment from the file
conda-create:
	conda env create -f conda.yml --name $(CONDA_ENV)

# exports all changes made locally - then one must copy the changes to conda.yml
conda-export:
	conda env export --from-history

# updates environment when some changes were applied to the file
conda-update:
	conda env update --file conda.yml --prune --name $(CONDA_ENV)

# does not actually work, has to be called manually
conda-activate:
	conda activate $(CONDA_ENV)

check-types:
	echo "Checking types" && \
		mypy backend tests

check-flake8:
	echo "Checking code style" && \
		flake8 backend tests

check-lint:
	echo "Linting code" && \
		pylint -j 0 backend tests

test:
	echo "Running tests" && \
		PROFILE=$${PROFILE:-profile/test.json} pytest

check: check-types check-flake8 check-lint test

init-venv:
	. ./venv/bin/activate

run-pipeline: conda-activate conda-update check-all

init-db-migrations:
# TODO: Yoyo
