# Common Module

This module serves as a shared code-base among other modules such as **worker** and **backend**.

## Setup

This module uses Python virtual environment only (not Conda).
To establish virtual environment **venv**, execute `make setup-dev`.
To (re)install packages from `requirements.txt`, execute `make install`.

## Development

There are defined various checks and tests (see `Makefile` for more details), all of
them can be called with `make check`.
