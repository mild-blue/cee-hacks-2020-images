# Backend Module

This module is responsible OCR processing, i.e., looking for unprocessed jobs to be executed.

## Setup

This module uses Conda.
1. Execute `make conda-create` which creates Conda env for you.
1. Execute `conda activate cee-hacks-2020-images-backend` to active environment.
1. To (re)install **common** module, execute `activate cee-hacks-2020-images-backend && pip install ../common`.

## Development

There are defined various checks and tests (see `Makefile` for more details), all of
them can be called with `make check`.
