# project settings
TOP := $(shell pwd)
PROJECT := webClient

##
# general
##

.PHONY: check-env clean

# verify we're inside a virtual environment
check-env:
ifndef VIRTUAL_ENV
	$(error "not in a virtualenv")
endif

# clean generated files
clean:
	find $(TOP) -name '*.pyc' -exec rm -rf {} \;

##
# testing
##

.PHONY: test test-unit

test: test-unit

test-unit: check-env
	py.test -v
