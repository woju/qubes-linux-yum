ifndef LOADING_PLUGINS
    ifneq (,$(findstring fc,$(DIST)))
	DISTRIBUTION := fedora

	ifeq ($(PACKAGE_SET),dom0)
            RPM_SPEC_FILES := rpm_spec/canadapop-repo-dom0.spec
    
        else ifeq ($(PACKAGE_SET),vm)
            RPM_SPEC_FILES := rpm_spec/canadapop-repo-vm.spec
        endif
    endif
endif

# vim: filetype=make
