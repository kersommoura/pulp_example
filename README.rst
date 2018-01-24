``pulp_example`` Plugin
=======================

This is the ``pulp_example`` Plugin for `Pulp Project
3.0+ <https://pypi.python.org/pypi/pulpcore/>`__. It is an example of
how to use the Pulp Plugin API to add a custom content type to Pulp.

All REST API examples below use `httpie <https://httpie.org/doc>`__ to perform the requests. The
``httpie`` commands below assume that the user executing the commands has a ``.netrc`` file in
the home directory. The ``.netrc`` should have the following configuration:

.. code-block::

    machine localhost
    login admin
    password admin

If you configured the ``admin`` user with a different password, adjust the configuration
accordingly. If you prefer to specify the username and password with each request, please see
``httpie`` documentation on how to do that. Also, the file permissions on ``.netrc`` should be 600
(readable/writable by owner only).

This documentation makes use of the `jq library <https://stedolan.github.io/jq/>`_
to parse the json received from requests, in order to get the unique urls generated
when objects are created. To follow this documentation as-is please install the jq
library with:

``$ sudo dnf install jq``

Install ``pulpcore``
--------------------

Follow the `installation
instructions <https://docs.pulpproject.org/en/3.0/nightly/installation/instructions.html>`__
provided with pulpcore.

Install ``pulp_example`` from source
------------------------------------

1)  sudo -u pulp -i
2)  source ~/pulpvenv/bin/activate
3)  git clone https://github.com/pulp/pulp\_example.git
4)  cd pulp\_example
5)  python setup.py develop
6)  pulp-manager makemigrations pulp\_example
7)  pulp-manager migrate pulp\_example
8)  django-admin runserver
9)  sudo systemctl restart pulp\_resource\_manager
10) sudo systemctl restart pulp\_worker@1
11) sudo systemctl restart pulp\_worker@2

Install ``pulp_example`` from PyPI
----------------------------------

1) sudo -u pulp -i
2) source ~/pulpvenv/bin/activate
3) pip install pulp-example
4) pulp-manager makemigrations pulp\_example
5) pulp-manager migrate pulp\_example
6) django-admin runserver
7) sudo systemctl restart pulp\_resource\_manager
8) sudo systemctl restart pulp\_worker@1
9) sudo systemctl restart pulp\_worker@2

Create a repository ``foo``
---------------------------

``$ http POST http://localhost:8000/api/v3/repositories/ name=foo``

.. code:: json

    {
        "_href": "http://localhost:8000/api/v3/repositories/8d7cd67a-9421-461f-9106-2df8e4854f5f/",
        ...
    }

``$ export REPO_HREF=$(http :8000/api/v3/repositories/ | jq -r '.results[] | select(.name == "foo") | ._href')``

Add an importer to repository ``foo``
-------------------------------------

``pulp_example`` provides two importer types: ``example-asyncio`` and
``example-futures``. Only one importer can be associated with the
repository.

An ``example-asyncio`` importer can be added to the repository ``foo``:

``$ http POST http://localhost:8000/api/v3/importers/example-asyncio/ name='bar' download_policy='immediate' sync_mode='mirror' feed_url='https://repos.fedorapeople.org/pulp/pulp/demo_repos/test_file_repo/PULP_MANIFEST' repository=$REPO_HREF``

.. code:: json

    {
        "_href": "http://localhost:8000/api/v3/importers/example-asyncio/$UUID/",
        ...
    }

``$ export ASYNCIO_IMPORTER_HREF=$(http :8000/api/v3/importers/example-asyncio/ | jq -r '.results[] | select(.name == "bar") | ._href')``

An ``example-futures`` importer can be added to the repository ``foo``:

``$ http POST http://localhost:8000/api/v3/importers/example-futures/ name='bar' download_policy='immediate' sync_mode='mirror' feed_url='https://repos.fedorapeople.org/pulp/pulp/demo_repos/test_file_repo/PULP_MANIFEST' repository=$REPO_HREF``

.. code:: json

    {
        "_href": "http://localhost:8000/api/v3/importers/example-futures/$UUID/",
        ...
    }


``$ export FUTURES_IMPORTER_HREF=$(http :8000/api/v3/importers/example-futures/ | jq -r '.results[] | select(.name == "bar") | ._href')``

Sync repository ``foo`` using importer ``bar``
----------------------------------------------

``example-asyncio`` importer:

``$ http POST $ASYNCIO_IMPORTER_HREF'sync/'``

``example-futures`` importer:

``$ http POST $FUTURES_IMPORTER_HREF'sync/'``

Upload ``foo.tar.gz`` to Pulp
-----------------------------

Create an Artifact by uploading the file to Pulp.

``$ http --form POST http://localhost:8000/api/v3/artifacts/ file@./foo.tar.gz``

.. code:: json

    {
        "_href": "http://localhost:8000/api/v3/artifacts/7d39e3f6-535a-4b6e-81e9-c83aa56aa19e/",
        ...
    }

Create ``example`` content from an Artifact
-------------------------------------------

Create a file with the json bellow and save it as content.json.

.. code:: json

    {
      "digest": "b5bb9d8014a0f9b1d61e21e796d78dccdf1352f23cd32812f4850b878ae4944c",
      "path": "foo.tar.gz",
      "artifacts": {"foo.tar.gz":"http://localhost:8000/api/v3/artifacts/7d39e3f6-535a-4b6e-81e9-c83aa56aa19e/"}
    }

``$ http POST http://localhost:8000/api/v3/content/example/ < content.json``

.. code:: json

    {
        "_href": "http://localhost:8000/api/v3/content/example/a9578a5f-c59f-4920-9497-8d1699c112ff/",
        "artifacts": {
            "foo.tar.gz": "http://localhost:8000/api/v3/artifacts/7d39e3f6-535a-4b6e-81e9-c83aa56aa19e/"
        },
        "digest": "b5bb9d8014a0f9b1d61e21e796d78dccdf1352f23cd32812f4850b878ae4944c",
        "notes": {},
        "path": "foo.tar.gz",
        "type": "example"
    }

Add content to repository ``foo``
---------------------------------

``$ http POST http://localhost:8000/api/v3/repositorycontents/ repository='http://localhost:8000/api/v3/repositories/foo/' content='http://localhost:8000/api/v3/content/example/a9578a5f-c59f-4920-9497-8d1699c112ff/'``

Currently there is no endpoint to manually associate content to a repository. This functionality
will be added before pulp3 beta is released.

Add an ``example`` Publisher to repository ``foo``
--------------------------------------------------

``$ http POST http://localhost:8000/api/v3/publishers/example/ name=bar repository=$REPO_HREF``

.. code:: json

    {
        "_href": "http://localhost:8000/api/v3/publishers/example/$UUID/",
        ...
    }

``$ export PUBLISHER_HREF=$(http :8000/api/v3/publishers/example/ | jq -r '.results[] | select(.name == "bar") | ._href')``

Create a Publication for Publisher ``bar``
------------------------------------------

``$ http POST http://localhost:8000/api/v3/publications/ publisher=$PUBLISHER_HREF``

.. code:: json

    [
        {
            "_href": "http://localhost:8000/api/v3/tasks/fd4cbecd-6c6a-4197-9cbe-4e45b0516309/",
            "task_id": "fd4cbecd-6c6a-4197-9cbe-4e45b0516309"
        }
    ]

``$ export PUBLICATION_HREF=$(http :8000/api/v3/publications/ | jq -r --arg PUBLISHER_HREF "$PUBLISHER_HREF" '.results[] | select(.publisher==$PUBLISHER_HREF) | ._href')``


Add a Distribution to Publisher ``bar``
---------------------------------------

``$ http POST http://localhost:8000/api/v3/distributions/ name='baz' base_path='foo' auto_updated=true http=true https=true publisher=$PUBLISHER_HREF publication=$PUBLICATION_HREF``


Check status of a task
----------------------

``$ http GET http://localhost:8000/api/v3/tasks/82e64412-47f8-4dd4-aa55-9de89a6c549b/``

Download ``test.iso`` from Pulp
---------------------------------

``$ http GET http://localhost:8000/content/foo/test.iso``
