===============
Getting started
===============

Installation
------------

Install from PyPI using pip::

    pip install pycodebase

Alternatively you can install the latest development version directly from GitHub::

    pip install https://github.com/davidwtbuxton/pycodebase/archive/master.zip


Connecting to Codebase
----------------------

You will need a Codebase API username and key.

::

    import codebase

    secrets = ('example/alice', 'topsecret')
    client = codebase.Client(secrets)

Instead of specifying your username / key in your program, you can create an INI file and then give the path to that file when creating the client.

The INI file should look like this::

    [api]
    username = example/alice
    key = topsecret

Then create the client with the path to the INI file. The filename can be a full path, a relative path or be relative to your home directory::

    import codebase

    secrets_filename = '~/.codebase.ini'
    client = codebase.Client.with_secrets(secrets_filename)


Common API Operations
---------------------

Once you have created a client with valid secrets, you are ready to interact with the Codebase API. Note that most client methods return a generator of results, and that API requests are made lazily (for example if results are paginated, the next request isn't made until your code accesses results on the second page).


Listing Projects
~~~~~~~~~~~~~~~~

Get information for all the projects in the account.

::

    projects = client.get_projects()

    for proj in projects:
        print 'Name', proj['project']['name']
        print 'ID', proj['project']['project_id']
        print 'Permalink', proj['project']['permalink']
