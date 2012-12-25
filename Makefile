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
	rm -f $(LIBDIR)/facebook/*.py
	rm -f $(LIBDIR)/util/*.py
	rm -f $(LIBDIR)/ui/*.py
uninstall:
	rm -rf $(LIBDIR)
	rm -f $(BINDIR)/eos-social
