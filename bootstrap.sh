#!/bin/sh

# Build React components
cd /usr/lib/ckan/ckanext-zarr/ckanext/zarr/react/ && \
    nvm install && \
    nvm use && \
    npm install && \
    npm run build

# Build fjelltopp theme sass files
FJELLTOPP_THEME="$CKAN_HOME/ckanext-fjelltopp-theme"
if [ -d "$FJELLTOPP_THEME" ]; then
  if [ "$CKAN_SITE_URL" = "http://zarr.minikube" ]; then
    echo "The Fjelltopp Theme $FJELLTOPP_THEME is enabled, compiling and start watching ..."
    npm --prefix "$FJELLTOPP_THEME" run compile
    npm --prefix "$FJELLTOPP_THEME" run watch &
  else
    echo "The Fjelltopp Theme $FJELLTOPP_THEME is enabled, compiling ..."
    npm --prefix "$FJELLTOPP_THEME" run compile
  fi
else
  echo "The Fjelltopp Theme $FJELLTOPP_THEME is not enabled."
fi
