#!/bin/sh

# Build React components
cd /usr/lib/ckan/ckanext-zarr/ckanext/zarr/react/ && \
    npm install && \
    npm run build

# Build fjelltopp theme sass files
FJELLTOPP_THEME="$CKAN_HOME/venv/src/ckanext-fjelltopp-theme"
if [ -d "$FJELLTOPP_THEME" ]; then
  cd $FJELLTOPP_THEME
  if [ "$CKAN_SITE_URL" = "http://zarr.minikube" ]; then
    echo "The Fjelltopp Theme $FJELLTOPP_THEME is enabled, compiling and start watching ..."
    npm run compile
    npm run watch &
  else
    echo "The Fjelltopp Theme $FJELLTOPP_THEME is enabled, compiling ..."
    npm run compile
  fi
else
  echo "The Fjelltopp Theme $FJELLTOPP_THEME is not enabled."
fi
