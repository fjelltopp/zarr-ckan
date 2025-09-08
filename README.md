# ZNRR CKAN Project

This repository contains the CKAN-based implementation for the Zambia National Research Repository (ZNRR). CKAN is an open-source data management system for powering data hubs and portals. For more information, see the [official CKAN documentation](https://docs.ckan.org/en/latest/).

## Project Structure

The main components of this repository are:

- `ckanext-zarr/` — Custom CKAN extension for ZNRR functionality.
  - `plugin.py` — CKAN plugin implementation
  - `actions.py` — Modified CKAN actions
  - `helpers.py` — Template helper functions
  - `presets.json` — ckanext-scheming extension presets
  - `profiles.py` — RDS-compatabile DCAT profile logic for Dublin Core Schema
  - `upload.py` — Giftless upload logic
  - `validators.py` — Custom validators
  - `assets/` — Static CSS and JS assets
  - `public/` — Public static images
  - `react/` — React frontend components: file uploader only
  - `schemas/` — DCAT-compatible Dublin Core Metadata Schema definitions
  - `templates/` — Jinja2 templates
  - `tests/` — Unit and integration tests
- `Dockerfile` — Containerization for reproducible deployments.
- `bootstrap.sh`, `ckan-entrypoint.sh` — Shell scripts for environment setup and container entrypoint.
- `Pipfile`, `Pipfile.lock` — Python dependency management using [Pipenv](https://pipenv.pypa.io/en/latest/).
- `.env` — Environment variable configuration (not committed; see below).
- `.github/` — CI/CD and development environment configuration.
- Submodules (3rd party):
  - `ckan/` — Core CKAN source code and configuration files.

## Dependency Management

- **Python dependencies** are managed with Pipenv (`Pipfile`, `Pipfile.lock`). This ensures reproducible environments and easy dependency updates. For extension development, `requirements.txt` and `dev-requirements.txt` are also provided.
- **Node.js dependencies** (for frontend assets in `ckanext-zarr/ckanext/zarr/react`) are managed via `package.json` in relevant directories.
- **Docker** is used for containerized deployments, ensuring consistency across environments.

## Environment Variables

Environment variables are loaded from the `.env` file (not committed to version control). Key variables typically include:

- `CKAN_SITE_URL` — The base URL for the CKAN instance.
- `CKAN_SQLALCHEMY_URL` — Database connection string.
- `CKAN_SOLR_URL` — Solr search engine URL.
- `CKAN_REDIS_URL` — Redis cache URL.
- `CKAN_DATASTORE_WRITE_URL` — Datastore write connection string.
- `CKAN_DATASTORE_READ_URL` — Datastore read connection string.
- Other extension-specific variables as required.

Refer to the [CKAN configuration documentation](https://docs.ckan.org/en/latest/maintaining/configuration.html) for a full list of supported environment variables.

## Code Best Practices

- **Follow CKAN extension development guidelines:** See [CKAN Extension Development](https://docs.ckan.org/en/latest/extensions/index.html).
- **Use Pipenv for Python dependency management:** Run `pipenv install` to set up the environment.
- **Linting and formatting:** Use `.flake8` for code style enforcement.
- **Testing:** Use `pytest` and CKAN's built-in test framework. Configuration files like `test-core.ini` are provided.
- **Version control:** Use `.gitignore` and to manage files in Git.
- **Documentation:** Update `README.md` and extension-specific `README.md` files regularly.

## Useful Links

- [CKAN Documentation](https://docs.ckan.org/en/latest/)
- [CKAN API Guide](https://docs.ckan.org/en/latest/api/index.html)
- [CKAN Extension Development](https://docs.ckan.org/en/latest/extensions/index.html)
- [CKAN Configuration](https://docs.ckan.org/en/latest/maintaining/configuration.html)

---

For questions or contributions, please refer to the individual extension `README.md` files or open an issue in this repository.
