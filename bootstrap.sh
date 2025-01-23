#!/bin/sh

# Build fjelltopp file uploader js and css files
FILE_UPLOADER="$CKAN_HOME/ckanext-file-uploader"
if [ -d "$FILE_UPLOADER" ]; then
  cd "$FILE_UPLOADER/react"
  if [ "$CKAN_SITE_URL" = "http://zarr.minikube" ]; then
    echo "The Fjelltopp CKAN Extension $FILE_UPLOADER is enabled, building and then watching ..."
    npm run build
    npm run dev &
  else
    echo "The Fjelltopp CKAN Extension $FILE_UPLOADER is enabled, building ..."
    npm run build
  fi
else
  echo "The Fjelltopp CKAN Extension $FILE_UPLOADER is not enabled."
fi

# Build fjelltopp theme sass files
FJELLTOPP_THEME="$CKAN_VENV/src/ckanext-fjelltopp-theme"
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
