#!/bin/sh
#
# Generate Python module for PyPi
# Called by ../../build_release.sh and depends on its actions
# Will also run in it's directory
# $1 is version number

LIBNAME="shoutcast_search"
PKGNAME=$LIBNAME-$1

echo "Generating pypi for $PKGNAME"

cd pkg/pypi

mkdir -p $PKGNAME/$LIBNAME
cat README | sed s/CURVERSION/$1/g > $PKGNAME/README
cat setup.py | sed s/CURVERSION/$1/g > $PKGNAME/setup.py
cat $LIBNAME/__init__.py | sed s/CURVERSION/$1/g > $PKGNAME/$LIBNAME/__init__.py
cat ../../shoutcast-search-$1/shoutcast_search.py | sed s/CURVERSION/$1/g > $PKGNAME/$LIBNAME/shoutcast_search.py


#rm -r $PKGNAME

cd ../../