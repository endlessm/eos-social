LIBDIR = $(DESTDIR)/usr/share/eos-social
BINDIR = $(DESTDIR)/usr/bin
clean:
	rm -f *.py[co] */*.py[co]
install:
	mkdir -p $(LIBDIR)
	mkdir -p $(BINDIR)
	cp -R src/* $(LIBDIR)
	cp eos-social $(BINDIR)
	chmod +X $(BINDIR)/eos-social
	python -m compileall $(LIBDIR)
	rm -f $(LIBDIR)/*.py
uninstall:
	rm -Rf /usr/lib/python2.7/dist-packages/eos-social
	rm -Rf $(LIBDIR)
	rm -f $(BINDIR)/eos-social
