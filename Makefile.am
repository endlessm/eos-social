SUBDIRS = EosSocial data

bin_SCRIPTS = eos-social

do_subst = sed -e 's|@pkglibdir[@]|$(pkglibdir)|g' \
               -e 's|@pkgdatadir[@]|$(pkgdatadir)|g' \
               -e 's|@GJS_CONSOLE[@]|$(GJS_CONSOLE)|g'

eos-social: eos-social.in Makefile
	$(AM_V_GEN) $(do_subst) $< > $@
	chmod +x $@

CLEANFILES = eos-social
EXTRA_DIST = eos-social.in
