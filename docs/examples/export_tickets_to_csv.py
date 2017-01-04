"""
This script shows how to get all tickets for a project and write ticket
data to a CSV file.

The username and key are saved in an INI file in ~/.codebase_secrets.ini:

    [api]
    username = example/alice
    key = 123abc456def789ghi

Use the script like this:

    $ python docs/example/export_tickets_to_csv.py my-project > tickets.csv

"""

import csv
import datetime
import sys

import codebase


def encode_dict(d, encoding='UTF-8'):
    """Converts unicode and datetime values to encoded strings."""
    result = {}

    for k, v in d.items():
        if isinstance(v, unicode):
            v = v.encode(encoding)
        elif isinstance(v, datetime.datetime):
            v = str(v)

        result[k] = v

    return result


def main(project_slug):
    client = codebase.Client.with_secrets('~/.codebase_secrets.ini')

    project = client.projects[project_slug]

    columns = [
        'ticket_id',
        'summary',
        'assignee',
        'status',
        'priority',
        'created_at',
        'updated_at',
    ]

    writer = csv.DictWriter(sys.stdout, columns, extrasaction='ignore')
    writer.writeheader()

    for ticket in project.tickets.values():
        row = vars(ticket)
        row['status'] = ticket.status['name']

        row = encode_dict(row)

        writer.writerow(row)


if __name__ == '__main__':
    project_slug = sys.argv[1]
    main(project_slug)
