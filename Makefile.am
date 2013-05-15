SUBDIRS = EosSocial

bin_SCRIPTS = eos-social

eos-social: eos-social.in Makefile
	$(AM_V_GEN)sed -e s!\@PYTHON\@!@PYTHON@!	\
	    -e s!\@PYOPTIONS\@!-OOt!			\
	    -e s!\@DATADIR\@!${datadir}!		\
	    < $< > $@
	chmod +x $@

CLEANFILES = eos-social
EXTRA_DIST = eos-social.in
