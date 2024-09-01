[![Tests](https://github.com/fjelltopp/ckanext-zarr/actions/workflows/test.yml/badge.svg)](https://github.com/fjelltopp/ckanext-zarr/actions/workflows/test.yml)

# ckanext-zarr

Provides tailored styling and features for CKAN for the Zambia Evaluation and Research Repository.


## Key features

The following key features are provided by this extension:

- Tailored UI styling
- Integration with Giftless and CKAN extensions ckanext-blob-storage, ckanext-authz-service and ckanext-versions for revisioning and release management
- Template changes to streamline the UI


## Configuration

To be written


## Installation

To install this extension:

1. Activate your CKAN virtual environment, for example:

     . /usr/lib/ckan/default/bin/activate

2. Clone the source and install it on the virtualenv

    git clone https://github.com/fjelltopp/ckanext-zarr.git
    cd ckanext-zarr
    pip install -e .
    pip install -r requirements.txt

3. Add `zarr` to the `ckan.plugins` setting in your CKAN
   config file (by default the config file is located at
   `/etc/ckan/default/ckan.ini`).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu:

     sudo service apache2 reload


## Developer installation

To install the extension for development, activate your CKAN virtualenv and
do:

    git clone https://github.com/fjelltopp/ckanext-zarr.git
    cd ckanext-zarr
    python setup.py develop
    pip install -r dev-requirements.txt


## Tests

To run the tests, do:

    pytest --ckan-ini=test.ini


## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
