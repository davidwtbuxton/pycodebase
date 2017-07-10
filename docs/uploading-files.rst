===============
Uploading files
===============


Attaching files to a ticket
---------------------------

Uploading files and attaching them to a ticket note is a two-step process.

First you upload the files, which will return information about file uploads, including the upload token for each file.

::

    import codebase

    secrets = ('example/alice', 'topsecret')
    client = codebase.Client(secrets)

    with open('screenshot.png') as pic:
        uploads = client.upload_files(files=[pic])

Second you create a ticket note and pass the newly-created file upload tokens. The response from the upload method is a generator of dictionaries, one for each uploaded file. Each dictionary has an 'identifier' key, the value of which is the token to use when referring to files with the Codebase API.

::

    upload_tokens = [obj['identifier'] for obj in uploads]
    ticket_id = 123
    client.create_ticket_note('myproject', ticket_id, upload_tokens=upload_tokens)
