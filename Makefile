define \n


endef

# project settings
TOP := $(shell pwd)
PROJECTS := brutus-api brutus-module-math brutus-module-weather brutus-module-jokes
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

run-% run-%-%:
	$(eval PROJECT := $(subst run,brutus,$@))
	$(eval BINARY := $(subst -,_,$(PROJECT)))
	$(eval CONFIG := $(TOP)/conf/$(PROJECT).sh)
	[ -f "${CONFIG}" ] && . "${CONFIG}" ; $(BINARY) --host 0.0.0.0

##
# testing
##

.PHONY: test test-style test-unit

test: test-style test-unit

test-style:
	@$(foreach project,$(PROJECTS), \
		$(MAKE) -C $(TOP)/src/$(project) test-style ${\n})

test-unit:
	@$(foreach project,$(PROJECTS), \
		$(MAKE) -C $(TOP)/src/$(project) test-unit ${\n})
