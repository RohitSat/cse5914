# project settings
TOP := $(shell pwd)
PROJECTS := brutus-api brutus-module-math brutus-module-weather

##
# general
##

.PHONY: clean distclean


# clean generated files
clean:
	@$(foreach project,$(PROJECTS), \
		cd src/$(project); \
		$(MAKE) clean; \
		cd $(TOP); )

# clean all development files
distclean:
	@$(foreach project,$(PROJECTS), \
		cd src/$(project); \
		$(MAKE) distclean; \
		cd $(TOP); )

##
# development
##

run-%:
	$(eval PROJECT := $(subst run,brutus,$@))
	$(eval BINARY := $(subst -,_,$(PROJECT)))
	$(eval CONFIG := $(TOP)/conf/$(PROJECT).sh)
	[ -f "${CONFIG}" ] && source "${CONFIG}" ; $(BINARY)

##
# testing
##

.PHONY: test test-style test-unit

test: test-style test-unit

test-style:
	@$(foreach project,$(PROJECTS), \
		cd src/$(project); \
		$(MAKE) test-style; \
		cd $(TOP); )

test-unit:
	@$(foreach project,$(PROJECTS), \
		cd src/$(project); \
		$(MAKE) test-unit; \
		cd $(TOP); )
