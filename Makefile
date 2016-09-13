# project settings
TOP := $(shell pwd)
PROJECTS := brutus-api brutus-module-math

##
# general
##

.PHONY: clean distclean


# clean generated files
clean:
	cd src/brutus-api && $(MAKE) clean
	cd src/brutus-module-math && $(MAKE) clean

# clean all development files
distclean:
	cd src/brutus-api && $(MAKE) distclean
	cd src/brutus-module-math && $(MAKE) distclean

##
# testing
##

.PHONY: test test-style test-unit

test: test-style test-unit

test-style:
	cd src/brutus-api && $(MAKE) test-style
	cd src/brutus-module-math && $(MAKE) test-style

test-unit:
	cd src/brutus-api && $(MAKE) test-unit
	cd src/brutus-module-math && $(MAKE) test-unit
