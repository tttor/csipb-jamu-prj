MODULE_NAME = gwaima
TARGET_NAMES := solve_mdp #solve simulate

ifdef HAS_ROOT_MAKEFILE

include .make/problem-template.mk

else
REDIRECT=$(MODULE_NAME)
.PHONY: $(MAKECMDGOALS) call-upwards
$(MAKECMDGOALS): call-upwards ;
call-upwards:
	@$(MAKE) --no-print-directory -C .. $(MAKECMDGOALS) REDIRECT=$(REDIRECT)
endif
