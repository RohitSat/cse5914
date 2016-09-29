# project settings
TOP := $(shell pwd)
PROJECT := brutus_module_weather

##
# general
##

.PHONY: check-env clean distclean

# verify we're inside a virtual environment
check-env:
ifndef VIRTUAL_ENV
	$(error "not in a virtualenv")
endif

# clean generated files
clean:
	find $(TOP) -name '*.pyc' -exec rm -rf {} \;

# clean all development files
distclean: clean
	rm -rf $(TOP)/$(PROJECT).egg-info
	rm -rf $(TOP)/build $(TOP)/dist

##
# testing
##

.PHONY: test test-style test-unit

test: test-style test-unit

test-style: check-env
	python setup.py egg_info > /dev/null
	pep8 --show-source --ignore=E125 --count \
		`cat $(PROJECT).egg-info/top_level.txt | xargs echo`

test-unit: check-env
	py.test -v
