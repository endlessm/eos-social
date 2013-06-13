autostartdir = $(sysconfdir)/xdg/autostart
autostart_DATA = eos-social-autostart.desktop

resource_files = $(shell $(GLIB_COMPILE_RESOURCES) --sourcedir=$(srcdir) --generate-dependencies $(srcdir)/eos-social.gresource.xml)
eos-social.gresource: eos-social.gresource.xml $(resource_files)
	$(AM_V_GEN) $(GLIB_COMPILE_RESOURCES) --target=$@ --sourcedir=$(srcdir) $<

resourcedir = $(pkgdatadir)
resource_DATA = eos-social.gresource

EXTRA_DIST = \
	eos-social.gresource.xml \
	$(autostart_DATA) \
	$(resource_files) \
	$(NULL)

CLEANFILES = \
	eos-social.gresource \
	$(NULL)
