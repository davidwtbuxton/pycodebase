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


Common API operations
---------------------

Once you have created a client with valid secrets, you are ready to interact with the Codebase API. Note that most client methods return a generator of results, and that API requests are made lazily (for example if results are paginated, the next request isn't made until your code accesses results on the second page).


Listing projects
~~~~~~~~~~~~~~~~

Get information for all the projects in the account.

::

    projects = client.get_projects()

    for proj in projects:
        print 'Name', proj['project']['name']
        print 'ID', proj['project']['project_id']
        print 'Permalink', proj['project']['permalink']


Finding a project's tickets
~~~~~~~~~~~~~~~~~~~~~~~~~~~

To interact with a project you refer to the project using its permalink. If the project's ticket page is https://example.codebasehq.com/projects/foo/tickets/ then its permalink is foo.

::

    tickets = client.get_tickets('foo')

    for ticket in tickets:
        print 'Ticket ID', ticket['ticket']['ticket_id']
        print 'Status', ticket['ticket']['status']['name']
        print 'Summary', ticket['ticket']['summary']
        print 'Last updated', ticket['ticket']['updated_at']


get_tickets accepts several keyword arguments for searching for tickets::

    ticket = client.get_tickets('foo', status='open')


Updating a ticket
~~~~~~~~~~~~~~~~~

Adding a note to an existing ticket is easy. You need to know the project's permalink and a valid ticket ID::

    summary = 'This appears as a new note. _Markdown is supported!_'
    client.create_ticket_note(project='foo', ticket_id=1234, summary=summary)

Changing the status or assigned user for a ticket is more complicated. You use the same create_ticket_note method, but you must know the ID for fields such as the status or the category.

Suppose your project has 3 statuses: "New", "In progress" and "Completed". First we get the statuses and their IDs::

    status_names_and_ids = {}
    statuses = client.get_ticket_statuses('foo')

    for status in statuses:
        status_name = status['ticketing_status']['name']
        status_id = status['ticketing_status']['id']

        status_names_and_ids[status_name] = status_id

Now we have a map of the status names and their object IDs, we can create a new note to change a ticket status to "Completed"::

    completed_id = status_names_and_ids['Completed']
    client.create_ticket_note(project='foo', ticket_id=1234, status_id=completed_id)
