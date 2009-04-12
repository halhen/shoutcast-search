#!/bin/sh
#
# Generate package for aur.archlinux.org
# Called by ../../build_release.sh and depends on its actions
# Will also run in it's directory
# $1 is version number

APPNAME="shoutcast-search"
RELEASENAME=$APPNAME-$1

echo "Generating www for $APPNAME"

cat $RELEASENAME/shoutcast-search.1 | nroff -man > releases/www/${RELEASENAME}.man.txt
cp releases/www/${RELEASENAME}.man.txt releases/www/${APPNAME}.man.txt
mkdir -p releases/www/dl/
cp releases/${RELEASENAME}.tar.gz releases/www/dl/
cp releases/${RELEASENAME}.tar.gz releases/www/dl/${APPNAME}-latest.tar.gz

(cat pkg/www/_header.html | sed s/PAGETITLE/shoutcast-search/; smu -n documentation.md; cat pkg/www/_footer.html) > releases/www/shoutcast-search.html
cp pkg/www/styles.css releases/www/