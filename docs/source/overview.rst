Secrets - CLI for secrets management
====================================

CLI application to manage a collection of secrets. The application manages two independent data objects:

- secrets
- service definition, referencing secrets

It allows for resolving secrets when displaying the service details. The goal is to be able to manage a collection
of services with some associated secrets, but keeping storage of both components independent.

It works in two modes:

- imports data from tables defined ``Emacs`` ``.org`` files, generating a database
  of ``services`` and ``secrets``. Both pieces have sensitive information, but the secrets
  are located in the ``secrets`` database, which must be conveniently protected.
  There is a built-in mechanism to encrypt the generated databases with a key.
- offers an interface to search for services, resolving ``usernames`` and ``passwords``
  from the ``secrets`` database.

The data is backed by a storage backend. Currently the only storage backend are plain json files,
protected with a key. There are plans to implement other storage backends.

Generate and save encryption key
--------------------------------

The key will be used to protect ``services`` and ``secrets`` (if given)::

    python manage.py generate-key > tmp/keyfile

Save the key in a secure place! It will be needed for working with the secrets.

Import data from the org files
------------------------------

To import the services::

    scripts/extract-org-table.el services data/services.org csv > tmp/services.csv
    scripts/extract-org-table.el questions data/services.org csv > tmp/questions.csv
    scripts/extract-org-table.el descriptions data/services.org csv > tmp/descriptions.csv
    python manage.py parse-services --keyfile tmp/keyfile --services tmp/services.csv --questions tmp/questions.csv --descriptions tmp/descriptions.csv > tmp/services.json

To import the secrets::

    scripts/extract-org-table.el secrets data/secrets.org csv > tmp/secrets.csv
    python manage.py parse-secrets --keyfile tmp/keyfile --secrets tmp/secrets.csv > tmp/secrets.json

The generated ``.json`` files have sensitive information (like the original ``.org`` files).
Those files should be handled accordingly (for example, encrypted with the ``keyfile``)

Searching for services
----------------------

To search for services and display secrets in plain text::

    python manage.py list-services --keyfile tmp/keyfile --resolve --services tmp/services.json --secrets tmp/secrets.json --regex <regex> --style table --mode compact
