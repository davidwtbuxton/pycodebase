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
import codebase.utils


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
        row['priority'] = ticket.priority['name']

        row = codebase.utils.encode_dict(row)

        writer.writerow(row)


if __name__ == '__main__':
    project_slug = sys.argv[1]
    main(project_slug)
