MODULE_NAME = problems

#jamusample activetag gwaima
#rocksample tag pushbox conttag
CHILD_DIRS := shared tag

ifdef HAS_ROOT_MAKEFILE

problems: $(CHILD_DIRS)

include .make/template.mk

else
REDIRECT=$(MODULE_NAME)
.PHONY: $(MAKECMDGOALS) call-upwards
$(MAKECMDGOALS): call-upwards ;
call-upwards:
	@$(MAKE) --no-print-directory -C .. $(MAKECMDGOALS) REDIRECT=$(REDIRECT)
endif
