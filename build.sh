#!/bin/bash -e
debuild -b -us -uc
rm -rf debian/endlessos-base-social
rm -f debian/*.log
rm -f debian/files
rm -r debian/*.substvars
mv ../*.deb .
mv ../*.changes .
mv ../*.build .
