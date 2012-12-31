LIBDIR = $(DESTDIR)/usr/share/eos-social
BINDIR = $(DESTDIR)/usr/bin
clean:
	rm -f *.py[co] */*.py[co]
install:
	mkdir -p $(LIBDIR)
	mkdir -p $(BINDIR)
	mkdir -p $(LIBDIR)/images
	cp -R src/* $(LIBDIR)
	cp -R images/* $(LIBDIR)/images
	cp eos-social $(BINDIR)
	chmod +X $(BINDIR)/eos-social
	python -m compileall $(LIBDIR)
	rm -f $(LIBDIR)/*.py
	rm -f $(LIBDIR)/facebook/*.py
	rm -f $(LIBDIR)/util/*.py
	rm -f $(LIBDIR)/ui/*.py
	mkdir -p $(DESTDIR)/usr/share/locale/pt_BR/LC_MESSAGES/
	msgfmt -v po/pt_BR.po -o $(DESTDIR)/usr/share/locale/pt_BR/LC_MESSAGES/eos-social.mo
uninstall:
	rm -f /usr/lib/python2.7/dist-packages/eos-social
	rm -Rf $(LIBDIR)
	rm -f $(BINDIR)/eos-social
	rm -Rf $(HOME)/.endlessm/social_bar/
