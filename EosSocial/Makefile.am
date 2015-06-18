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

libeossocialprivate_1_0_la_CPPFLAGS = \
	$(EOS_SOCIAL_CFLAGS)
libeossocialprivate_1_0_la_LIBADD = \
	$(EOS_SOCIAL_LIBS)
libeossocialprivate_1_0_la_LDFLAGS = \
	-avoid-version

libeossocialprivate_1_0_la_SOURCES = \
	eossocialutils.h \
	eossocialutils.c

pkglib_LTLIBRARIES = libeossocialprivate-1.0.la

include $(INTROSPECTION_MAKEFILE)
INTROSPECTION_GIRS = EosSocialPrivate-1.0.gir

girdir = $(pkgdatadir)/gir-1.0
gir_DATA = $(INTROSPECTION_GIRS)

typelibdir = $(pkglibdir)/girepository-1.0
typelib_DATA = $(gir_DATA:.gir=.typelib)

EosSocialPrivate-1.0.gir: libeossocialprivate-1.0.la Makefile
EosSocialPrivate_1_0_gir_NAMESPACE = EosSocialPrivate
EosSocialPrivate_1_0_gir_VERSION = 1.0
EosSocialPrivate_1_0_gir_LIBS = libeossocialprivate-1.0.la
EosSocialPrivate_1_0_gir_CFLAGS = $(AM_CPPFLAGS) $(EOS_SOCIAL_CFLAGS)
EosSocialPrivate_1_0_gir_SCANNERFLAGS = --warn-all --symbol-prefix=eos_social --identifier-prefix=EosSocial
EosSocialPrivate_1_0_gir_INCLUDES = \
	WebKit2-4.0
EosSocialPrivate_1_0_gir_FILES = \
    $(addprefix $(srcdir)/,$(libeossocialprivate_1_0_la_SOURCES))


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
	$(gir_DATA) \
	$(typelib_DATA) \
	$(NULL)
