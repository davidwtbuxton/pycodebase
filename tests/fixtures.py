# encoding: utf-8
import json


project_response = json.dumps(
    [
        {
            'project': {
                'account_name': 'Example',
                'closed_tickets': 25,
                'disk_usage': 100196,
                'group_id': 'FooGroup',
                'icon': 4,
                'name': 'Foo',
                'open_tickets': 75,
                'overview': None,
                'permalink': 'foo',
                'project_id': 1234,
                'start_page': 'overview',
                'status': 'active',
                'total_tickets': 100,
            },
        },
    ]
)

ticket_response = json.dumps(
    [
        {
            "ticket": {
                "ticket_id": 123,
                "summary": "Summary of ticket",
                "ticket_type": "Feature",
                "reporter_id": 163370,
                "assignee_id": 163370,
                "assignee": "alice-example",
                "reporter": "alice-example",
                "category_id": 6660202,
                "category": {
                    "id": 6660202,
                    "name": "FE",
                },
                "priority_id": 6517669,
                "priority": {
                    "id": 6517669,
                    "name": "Normal",
                    "colour": "blue",
                    "default": True,
                    "position": 3,
                },
                "status_id": 6517639,
                "status": {
                    "id": 6517639,
                    "name": "New",
                    "colour": "green",
                    "order": 1,
                    "treat-as-closed": False,
                },
                "type_id": 6517696,
                "type": {
                    "id": 6517696,
                    "name": "Feature",
                    "icon": "construction",
                },
                "milestone_id": 210655,
                "milestone": {
                    "id": 210655,
                    "identifier": "cbf790b0-a170-f987-6a81-7d9b02c415a9",
                    "name": "Sprint 1",
                    "start_at": "2016-12-15",
                    "deadline": "2017-01-04",
                    "parent_id": None,
                    "description": "Description of milestone",
                    "responsible_user_id": 60754,
                    "estimated_time": 1000,
                    "status": "active",
                },
                "start_on": None,
                "deadline": None,
                "tags": "",
                "updated_at": "2016-12-21T16:50:04Z",
                "created_at": "2016-09-28T08:48:07Z",
                "estimated_time": 600,
                "project_id": 162613,
                "total_time_spent": 0,
            },
        },
    ]
)

repository_response = json.dumps(
    [
        {
            "repository": {
                "default_branch": "master",
                "disk_usage": 224968704,
                "last_commit_ref": "abc9350159b4543b3ac0927a57d8b2075a3651e7",
                "clone_url": "git@codebasehq.com:example/foo/foo-code-repo.git",
                "name": "Foo Code Repo",
                "permalink": "foo-code-repo",
                "description": None,
                "scm": "git",
            },
        },
    ]
)


commit_response = json.dumps(
    [
        {
            "commit": {
                "ref": "abc9350159b4543b3ac0927a57d8b2075a312345",
                "author_email": "alice@example.com",
                "author_name": "Alice A",
                "authored_at": "2017-12-31T14:03:03+01:00",
                "committed_at": "2017-12-31T14:03:03+01:00",
                "committer_email": "alice@example.com",
                "committer_name": "Alice A",
                "message": "Rewrite Kevin's code",
                "parent_ref": "pqr9350159b4543b3ac0927a57d8b2075a312345",
                "tree_ref": "xyz9350159b4543b3ac0927a57d8b2075a312345",
                "author_user": "alice",
                "committer_user": "alice"
            },
        },
    ]
)


deployment_response = json.dumps(
    [
        {
            "deployment": {
                "branch": "master",
                "environment": "Live",
                "revision": "abc8d7171187341f02e47319bfb0950d23209731",
                "servers": "example.com"
            },
        },
    ]
)


ticket_priority_response = json.dumps(
    [
        {
            "ticketing_priority": {
                "id": 1234567,
                "name": "Normal",
                "colour": "green",
                "default": False,
                "position": 3,
            },
        },
    ]
)

ticket_category_response = json.dumps(
    [
        {
            "ticketing_category": {
                "id": 1234567,
                "name": "Security",
            },
        },
    ]
)

ticket_status_response = json.dumps(
    [
        {
            "ticketing_status": {
                "id": 1234567,
                "name": "In progress",
                "colour": "orange",
                "order": 1,
                "treat_as_closed": False
            },
        },
    ]
)

ticket_type_response = json.dumps(
    [
        {
            "ticketing_type": {
                "id": 1234567,
                "name": "Bug",
                "icon": "bug",
            },
        },
    ]
)

ticket_note_response = json.dumps(
    [
        {
            "ticket_note": {
                "attachments": [
                    {
                        "id": 1234567,
                        "identifier": "abcdefgh-7b10-226d-c486-40a7008c72ea",
                        "file-name": "Attachement name.png",
                        "content-type": "image/png",
                        "file-size": 207599,
                        "url": "https://example.codebasehq.com/upload/uuid-goes-here/show/original"
                    }
                ],
                "content": "A comment on a ticket note",
                "created_at": "2016-12-14T16:42:51Z",
                "updated_at": "2016-12-14T16:42:51Z",
                "id": 1234567,
                "user_id": 12345,
                "updates": "{}"
            },
        },
    ]
)

project_user_response = json.dumps(
    [
        {
            "user": {
                "company": "Example",
                "first_name": "Alice",
                "last_name": "A",
                "id": 12345,
                "username": "alice",
                "email_address": "alice@example.com",
                "email_addresses": [
                    "alice@example.com",
                ]
            },
        },
    ]
)

# This fixture is used for testing Client.get_activity() and
# Client.get_project_activity().
activity_response = json.dumps(
    [
        {
            u'event': {
                u'actor_email': u'alice@example.com',
                u'actor_name': u'Alice A',
                u'avatar_url': u'https://identity.atechmedia.com/avatar/123/45',
                u'deleted': False,
                u'html_text': u'<ul class="changes"><li>Foo</li></ul>',
                u'html_title': u'<a href=\'/users/123\' class=\'text--link\'>Alice A</a>',
                u'id': 123456789,
                u'project_id': 123456,
                u'raw_properties': {
                    u'changes': {
                        u'ticket_type_id': [u'Feature', u'Task'],
                    },
                    u'content': u'',
                    u'criteria': {
                        u'added': None,
                      u'changed': None,
                      u'removed': None,
                      u'satisfied': None,
                      u'unsatisfied': None,
                    },
                    u'number': 999,
                    u'project_name': u'Foo',
                    u'project_permalink': u'foo',
                    u'source': None,
                    u'source_ref': None,
                    u'subject': u'Ticket title.',
                    u'time_added': u'',
                    u'verb': None},
                u'timestamp': u'2017-01-05 16:30:51 UTC',
                u'title': u'Alice A updated #999 Ticket title.',
                u'type': u'ticketing_note',
                u'user_id': 12345,
            }
        },
    ]
)


public_keys_response = json.dumps(
    [
        {
            u'public_key_join': {
                u'description': u'Regular key',
                u'key': u'ssh-rsa abc==',
            },
        },
    ]
)

milestones_response = json.dumps(
    [
        {
            'ticketing_milestone': {
                u'deadline': None,
                u'description': u'',
                u'estimated_time': 0,
                u'id': 123,
                u'identifier': u'123-4-5-6-uuid',
                u'name': u'Bar milestone',
                u'parent_id': None,
                u'responsible_user_id': 987,
                u'start_at': None,
                u'status': u'active',
            },
        },
    ]
)
