dnl -*- Mode: autoconf -*-
dnl Process this file with autoconf to produce a configure script.
AC_PREREQ(2.53)
AC_INIT([eos-social], [1.0.99], [http://www.endlessm.com])
m4_ifdef([AM_SILENT_RULES],[AM_SILENT_RULES([yes])])
AC_CONFIG_SRCDIR([EosSocial/main.js])
AC_CONFIG_HEADERS([config.h])
AM_INIT_AUTOMAKE([1.9 no-dist-gzip dist-xz foreign tar-ustar])

GETTEXT_PACKAGE=AC_PACKAGE_NAME
AC_SUBST(GETTEXT_PACKAGE)
AC_DEFINE_UNQUOTED(GETTEXT_PACKAGE,"$GETTEXT_PACKAGE",[The name of the gettext domain])
IT_PROG_INTLTOOL(0.40.0)

# enable libtool
AC_PROG_LIBTOOL

GOBJECT_INTROSPECTION_REQUIRE([0.9.6])

PKG_CHECK_MODULES(EOS_SOCIAL,
                  gjs-1.0
                  gio-2.0
                  gtk+-3.0
                  webkit2gtk-4.0)


GJS_CONSOLE=`$PKG_CONFIG --variable=gjs_console gjs-1.0`
AC_SUBST(GJS_CONSOLE)

GLIB_COMPILE_RESOURCES=`$PKG_CONFIG --variable glib_compile_resources gio-2.0`
AC_SUBST(GLIB_COMPILE_RESOURCES)

AC_CONFIG_FILES([
        Makefile
        data/Makefile
        EosSocial/Makefile
        po/Makefile.in
        ])

AC_OUTPUT
echo "
        eos-social $VERSION
        ===================

        prefix: ${prefix}

        Now type 'make' to build $PACKAGE
"
