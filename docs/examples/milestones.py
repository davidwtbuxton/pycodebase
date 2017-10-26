from __future__ import print_function

"""
How to get and create milestones.

Usage:

    python milestones.py foo-project
    python milestones.py foo-project --name="My new milestone"
"""
import argparse
import sys

import codebase


def main(project, **kwargs):
    client = codebase.Client.with_secrets('~/.codebase_secrets.ini')

    if any(kwargs.values()):
        result = client.create_milestone(project, **kwargs)
        print('Created milestone')
        print(result)

    for milestone_dict in client.get_milestones(project):
        print(milestone_dict)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('project')

    milestone_fields = ('deadline', 'description', 'estimated_time', 'name',
        'parent_id', 'responsible_user_id', 'start_at', 'status')

    for field in milestone_fields:
        option_name = '--' + field
        parser.add_argument(option_name)

    kwargs = vars(parser.parse_args())

    main(**kwargs)
