jsdir = $(pkgdatadir)/js/
dist_js_DATA = \
	$(BUILT_SOURCES) \
	main.js \
	socialBar.js \
	socialBarView.js \
	parseUri.js \
	wmInspect.js \
	$(NULL)

do_path_subst = sed \
	-e 's|@pkgdatadir[@]|$(pkgdatadir)|g' \
	-e 's|@localedir[@]|$(localedir)|g'
path.js: Makefile path.js.in
	$(AM_V_GEN) $(do_path_subst) $(srcdir)/path.js.in > $@

do_config_subst = sed \
	-e 's|@PACKAGE_NAME[@]|$(PACKAGE)|g' \
	-e 's|@PACKAGE_VERSION[@]|$(VERSION)|g' \
	-e 's|@GETTEXT_PACKAGE[@]|$(GETTEXT_PACKAGE)|g'
config.js: Makefile config.js.in
	$(AM_V_GEN) $(do_config_subst) $(srcdir)/config.js.in > $@

BUILT_SOURCES = \
	config.js \
	path.js \
	$(NULL)

EXTRA_DIST = \
	config.js.in \
	path.js.in \
	$(NULL)

CLEANFILES = \
	config.js \
	path.js \
	$(NULL)
