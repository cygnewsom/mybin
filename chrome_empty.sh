#!/bin/bash
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3325.181 Safari/537.36"
TMPDIR=`mktemp -d`
DEFAULTDIR="$TMPDIR/Default"

mkdir -p "$DEFAULTDIR"
cp -rv $HOME/scripts/Default/* "$DEFAULTDIR/"

/usr/bin/chromium-browser --no-first-run --user-data-dir="$TMPDIR" --user-agent="$UA"

find $TMPDIR -type f -exec shred -n3 -zu {} \;
rm -rf "$TMPDIR"
