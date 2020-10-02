# Klaro Services Database

This is a database of third-party services that Klaro and its backend uses to
manage them. Every entry in the database is identified by a unique name.

## Installing Requirements

To create a Python virtual environment install requirements, simply run

    make setup

## Packing the Database

The database is stitched together from a collection of YAML files. To add a new
service, simply create a YAML-file for it and include it in the list of files
in `index.yml`. To create the `database.json` file, simply run

    make database

## Synchronizing the Database

To synchronize the database with the API, simply run

    TOKEN=[access token] API=[api base URL] make sync

This will upload all services to the backend database. For the production
version, the API address is `https://api.kiprotect.com`.