#!/bin/sh
# build js components & allow editing

# Build fjelltopp theme sass files
FJELLTOPP_THEME="$CKAN_HOME/ckanext-fjelltopp-theme"

if [ -d "$FJELLTOPP_THEME" ]; then
  echo "The Fjelltopp Theme $FJELLTOPP_THEME is enabled, compiling ..."
  npm --prefix "$FJELLTOPP_THEME" run compile
  npm --prefix "$FJELLTOPP_THEME" run watch &
else
  echo "The Fjelltopp Theme $FJELLTOPP_THEME is not enabled."
fi
