dnl -*- Mode: autoconf -*-
dnl Process this file with autoconf to produce a configure script.
AC_PREREQ(2.53)
AC_INIT([eos-social], [1.0.99], [http://www.endlessm.com])
m4_ifdef([AM_SILENT_RULES],[AM_SILENT_RULES([yes])])
AC_CONFIG_SRCDIR(eos-social.in)
AC_CONFIG_HEADERS([config.h])
AM_INIT_AUTOMAKE([1.9 no-dist-gzip dist-xz foreign])

AM_PATH_PYTHON_VERSION(2.7, 2.7.0, 2.6, 2.6.0, 2.5, 2.5.0, 2.4, 2.4.0)

GOBJECT_INTROSPECTION_REQUIRE([0.9.6])

PKG_CHECK_MODULES(EOS_SOCIAL,
                  gio-2.0
                  gtk+-3.0
                  webkitgtk-3.0
                  gobject-introspection-1.0)

AC_CONFIG_FILES([
        Makefile
        EosSocial/Makefile
        ])

AC_OUTPUT
echo "
        eos-social $VERSION
        ===================

        prefix: ${prefix}

        Now type 'make' to build $PACKAGE
"
