#!/bin/bash -e
debuild -b -us -uc
rm -rf debian/eos-social
rm -f debian/eos-social.debhelper.log
rm -f debian/files
rm -r debian/eos-social.substvars
mv ../*.deb .
mv ../*.changes .
mv ../*.build .
