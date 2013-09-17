resource_files = $(shell $(GLIB_COMPILE_RESOURCES) --sourcedir=$(srcdir) --generate-dependencies $(srcdir)/eos-social.gresource.xml)
eos-social.gresource: eos-social.gresource.xml $(resource_files)
	$(AM_V_GEN) $(GLIB_COMPILE_RESOURCES) --target=$@ --sourcedir=$(srcdir) $<

resourcedir = $(pkgdatadir)
resource_DATA = eos-social.gresource

servicedir = $(datadir)/dbus-1/services
service_DATA = $(service_in_files:.service.in=.service)
service_in_files = \
	com.endlessm.SocialBar.service.in \
	$(NULL)
com.endlessm.SocialBar.service: com.endlessm.SocialBar.service.in Makefile
	$(AM_V_GEN) sed -e "s|\@libexecdir\@|$(libexecdir)|" $< > $@

EXTRA_DIST = \
	eos-social.gresource.xml \
	$(resource_files) \
	$(service_in_files) \
	$(NULL)

CLEANFILES = \
	eos-social.gresource \
	$(service_DATA) \
	$(NULL)
