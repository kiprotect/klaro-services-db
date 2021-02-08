# Klaro Services Database

This is a database of third-party services that Klaro and its backend uses to
manage them. Every entry in the database is identified by a unique name.

## License

This database is licensed under the Creative Commons Attribution-NoDerivatives
4.0 International license (CC BY-ND). In a nutshell, this means that you can reuse
this database for any purpose, including commercially; however, it cannot be shared
with others in adapted form, and credit must be provided to this project. A full
copy of the license text can be found on the [Creative Commons website](https://creativecommons.org/licenses/by-nd/4.0/legalcode).

### Attribution

If you use this database in conjunction with the open-source version of Klaro,
it suffices to leave the "Realized with Klaro!" link in the consent modal
(which is enabled by default, so you don't need to do anything).

If you use this database in a software tool, you may link either to this Github
page or the [Klaro website](https://kiprotect.com/klaro) from the main page
of your documentation, your README (in case the software is open-source) or
the software itself.

## Contributing

If you want to contribute to this database (which we'd love you to do), please
edit/create the relevant database entries and open a pull request. You will
have to sign a Contributor License Agreement (CLA) before we can merge your PR.

## Installing Requirements

To create a Python virtual environment install requirements, simply run

    make setup

## Packing the Database

The database is stitched together from a collection of YAML files. To add a new
service, simply create a YAML-file for it and include it in the list of files
in `index.yml`. To create the `database.json` file, simply run

    make database

## Synchronizing the Service Database

To synchronize the database with the API, simply run

    TOKEN=[access token] API=[api base URL] make sync

This will upload all services to the backend database. For the production
version, the API address is `https://api.kiprotect.com`. For the local
version, you should go to the "Account Settings" app, click on "Access Tokens"
and create a new token with the `kiprotect:api:klaro:services` scope.
