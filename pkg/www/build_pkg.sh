#!/bin/sh
#
# Generate package for aur.archlinux.org
# Called by ../../build_release.sh and depends on its actions
# Will also run in it's directory
# $1 is version number

APPNAME="shoutcast-search"
RELEASENAME=$APPNAME-$1

echo "Generating www for $APPNAME"

cat $RELEASENAME/shoutcast-search.1 | nroff -man | man2html -title "$RELEASENAME" > releases/www/${RELEASENAME}.man.html
cp releases/${RELEASENAME}.tar.gz releases/www/