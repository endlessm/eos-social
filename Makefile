LIBDIR = $(DESTDIR)/usr/share/eos-social
BINDIR = $(DESTDIR)/usr/bin
CFGDIR = $(DESTDIR)/etc/eos-social
clean:
	rm -f *.py[co] */*.py[co]
install:
	mkdir -p $(LIBDIR)
	mkdir -p $(BINDIR)
	mkdir -p $(CFGDIR)
	mkdir -p $(LIBDIR)/images
	cp -R src/* $(LIBDIR)
	cp etc/eos-social/* $(CFGDIR)
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
	rm -Rf /usr/lib/python2.7/dist-packages/eos-social
	rm -Rf $(LIBDIR)
	rm -Rf $(CFGDIR)
	rm -f $(BINDIR)/eos-social
	rm -Rf $(HOME)/.endlessm/social_bar/
