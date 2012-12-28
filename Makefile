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
uninstall:
	rm -f /usr/lib/python2.7/dist-packages/eos-social
	rm -rf $(LIBDIR)
	rm -f $(BINDIR)/eos-social
	rm -rf $(HOME)/.endlessm/social_bar/
