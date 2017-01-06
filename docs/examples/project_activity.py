"""
This script gets any events from a project's activities feed, up to
7 days ago.

The time and event's title are printed to the console.
"""

import datetime
import sys

import codebase


def main(project_slug):
    client = codebase.Client.with_secrets('~/.codebase_secrets.ini')

    # We'll ask for the past 7 days.
    since = datetime.datetime.now() - datetime.timedelta(days=7)
    activity = client.get_project_activity(project_slug, since=since)

    for idx, obj in enumerate(activity, 1):
        # Look at `project_activity_response` in tests/test_codebase.py for an
        # example of the event resource (when raw=False).
        event = obj['event']
        print idx, event['timestamp'], event['type'], event['title']


if __name__ == '__main__':
    main(sys.argv[1])
