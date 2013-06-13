jsdir = $(pkgdatadir)/js/
dist_js_DATA = \
	$(BUILT_SOURCES) \
	frameClock.js \
	main.js \
	socialBar.js \
	socialBarView.js \
	parseUri.js \
	wmInspect.js \
	$(NULL)

do_subst = sed -e 's|@pkgdatadir[@]|$(pkgdatadir)|g'
path.js: Makefile path.js.in
	$(AM_V_GEN) $(do_subst) $(srcdir)/path.js.in > $@

BUILT_SOURCES = \
	path.js \
	$(NULL)

EXTRA_DIST = \
	path.js.in \
	$(NULL)
