# encoding: utf-8
import json
import os
import tempfile
import types
import unittest

import httpretty

import codebase


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


class ClientTestCase(unittest.TestCase):
    def test_client_properties(self):
        obj = codebase.Client(('example/alice', 'secret'))

        obj.projects
        obj.create_deployment
        obj.create_ticket
        obj.create_ticket_note
        obj.get_activity
        obj.get_deployments
        obj.get_project_activity
        obj.get_projects
        obj.get_repositories
        obj.get_ticket_categories
        obj.get_ticket_notes
        obj.get_ticket_priorities
        obj.get_ticket_statuses
        obj.get_ticket_types
        obj.get_tickets

    @httpretty.activate
    def test_get_projects_returns_generator_of_projects(self):
        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/projects',
            body=project_response,
            content_type='application/json',
        )

        obj = codebase.Client(('example/alice', 'secret'))
        result = obj.get_projects()

        self.assertIsInstance(result, types.GeneratorType)

    @httpretty.activate
    def test_get_project_activity_returns_generator_of_activity(self):
        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/foo/activity',
            responses=[
                httpretty.Response(body=activity_response, content_type='application/json'),
                httpretty.Response(body=json.dumps([]), content_type='application/json'),
            ],
        )

        obj = codebase.Client(('example/alice', 'secret'))
        result = obj.get_project_activity('foo')

        self.assertIsInstance(result, types.GeneratorType)

        activities = list(result)

        self.assertEqual(len(activities), 1)
        self.assertEqual(activities[0]['event']['actor_name'], u'Alice A')

    @httpretty.activate
    def test_get_account_activity_returns_generator_of_activity(self):
        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/activity',
            responses=[
                httpretty.Response(body=activity_response, content_type='application/json'),
                httpretty.Response(body=json.dumps([]), content_type='application/json'),
            ],
        )

        obj = codebase.Client(('example/alice', 'secret'))
        result = obj.get_activity()

        self.assertIsInstance(result, types.GeneratorType)

        activities = list(result)

        self.assertEqual(len(activities), 1)
        self.assertEqual(activities[0]['event']['actor_name'], u'Alice A')

    def test_create_new_client_from_secrets_file(self):
        with tempfile.NamedTemporaryFile(delete=False) as fh:
            filename = fh.name
            fh.write('[api]\nusername = example/alice\nkey = secret\n')

        try:
            client = codebase.Client.with_secrets(filename)
        finally:
            os.unlink(filename)

        self.assertEqual(client.auth, ('example/alice', 'secret'))


class ProjectTestCase(unittest.TestCase):
    @httpretty.activate
    def test_projects_returns_map_of_projects(self):
        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/projects',
            body=project_response,
            content_type='application/json',
        )

        obj = codebase.Client(('example/alice', 'secret'))
        result = len(obj.projects)

        self.assertEqual(result, 1)

    @httpretty.activate
    def test_projects_can_be_indexed_by_permalink(self):
        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/projects',
            body=project_response,
            content_type='application/json',
        )

        obj = codebase.Client(('example/alice', 'secret'))
        result = obj.projects['foo']

        self.assertIsInstance(result, codebase.Project)

    def test_project_as_repr(self):
        obj = codebase.Project(project_id=123, name=u'Olé')
        result = repr(obj)
        expected = "Project(project_id=123, name=u'Ol\\xe9')"

        self.assertEqual(result, expected)


class ProjectUserTestCase(unittest.TestCase):
    @httpretty.activate
    def test_users_returns_map_of_assigned_users(self):
        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/projects',
            body=project_response,
            content_type='application/json',
        )

        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/foo/assignments',
            body=project_user_response,
            content_type='application/json',
        )

        obj = codebase.Client(('example/alice', 'secret'))
        foo_proj = obj.projects['foo']
        assigned_users = foo_proj.users.values()

        self.assertEqual(len(assigned_users), 1)
        self.assertIsInstance(assigned_users[0], codebase.User)
        self.assertEqual(
            vars(assigned_users[0]),
            {
                '_client': None,
                'company': u'Example',
                'email_address': u'alice@example.com',
                'email_addresses': [u'alice@example.com'],
                'first_name': u'Alice',
                'id': 12345,
                'last_name': u'A',
                'username': u'alice',
            },
        )


class TicketTestCase(unittest.TestCase):
    @httpretty.activate
    def test_tickets_returns_map_of_tickets(self):
        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/projects',
            body=project_response,
            content_type='application/json',
        )

        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/foo/tickets',
            responses=[
                httpretty.Response(body=ticket_response, status=200, content_type='application/json'),
                httpretty.Response(body=json.dumps([]), status=404, content_type='application/json'),
            ],
        )

        obj = codebase.Client(('example/alice', 'secret'))
        foo_proj = obj.projects['foo']
        result = len(foo_proj.tickets)

        self.assertEqual(result, 1)

    @httpretty.activate
    def test_tickets_can_be_indexed_by_id(self):
        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/projects',
            body=project_response,
            content_type='application/json',
        )

        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/foo/tickets',
            responses=[
                httpretty.Response(body=ticket_response, status=200, content_type='application/json'),
                httpretty.Response(body=json.dumps([]), status=404, content_type='application/json'),
            ],
        )

        obj = codebase.Client(('example/alice', 'secret'))
        foo_proj = obj.projects['foo']
        result = foo_proj.tickets[123]

        self.assertIsInstance(result, codebase.Ticket)

    def test_ticket_as_repr(self):
        obj = codebase.Ticket(ticket_id=123)
        result = repr(obj)

        self.assertEqual(result, 'Ticket(ticket_id=123)')


class NoteTestCase(unittest.TestCase):
    @httpretty.activate
    def test_ticket_notes_returns_map_of_notes(self):
        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/projects',
            body=project_response,
            content_type='application/json',
        )

        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/foo/tickets',
            responses=[
                httpretty.Response(body=ticket_response, status=200, content_type='application/json'),
                httpretty.Response(body=json.dumps([]), status=404, content_type='application/json'),
            ],
        )

        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/foo/tickets/123/notes',
            body=ticket_note_response,
            content_type='application/json',
        )

        obj = codebase.Client(('example/alice', 'secret'))
        foo_proj = obj.projects['foo']
        ticket = foo_proj.tickets[123]
        notes = list(ticket.notes)

        self.assertEqual(len(notes), 1)


class RepositoryTestCase(unittest.TestCase):
    @httpretty.activate
    def test_repositories_returns_map_of_repos(self):
        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/projects',
            body=project_response,
            content_type='application/json',
        )

        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/foo/repositories',
            body=repository_response,
            content_type='application/json',
        )

        obj = codebase.Client(('example/alice', 'secret'))
        foo_proj = obj.projects['foo']
        result = len(foo_proj.repositories)

        self.assertEqual(result, 1)

    def test_repository_as_repr(self):
        obj = codebase.Repository(clone_url='git@codebasehq.com:example/foo/foo-code.git')
        result = repr(obj)
        expected = "Repository(clone_url='git@codebasehq.com:example/foo/foo-code.git')"

        self.assertEqual(result, expected)

    @httpretty.activate
    def test_repositories_can_be_indexed_by_permalink(self):
        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/projects',
            body=project_response,
            content_type='application/json',
        )

        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/foo/repositories',
            body=repository_response,
            content_type='application/json',
        )

        obj = codebase.Client(('example/alice', 'secret'))
        foo_proj = obj.projects['foo']
        result = foo_proj.repositories['foo-code-repo']

        self.assertIsInstance(result, codebase.Repository)


class DeploymentTestCase(unittest.TestCase):
    @httpretty.activate
    def test_deployments_returns_a_map_of_deployments(self):
        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/projects',
            body=project_response,
            content_type='application/json',
        )

        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/foo/repositories',
            body=repository_response,
            content_type='application/json',
        )

        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/foo/foo-code-repo/deployments',
            responses=[
                httpretty.Response(body=deployment_response, content_type='application/json'),
                httpretty.Response(body=json.dumps([]), content_type='application/json'),
            ],
        )

        obj = codebase.Client(('example/alice', 'secret'))
        foo_proj = obj.projects['foo']
        foo_repo = foo_proj.repositories['foo-code-repo']
        foo_deployments = foo_repo.deployments

        self.assertEqual(len(foo_deployments), 1)


class TicketStatusTestCase(unittest.TestCase):
    @httpretty.activate
    def test_project_statuses_returns_map_of_statuses(self):
        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/projects',
            body=project_response,
            content_type='application/json',
        )

        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/foo/tickets/statuses',
            body=ticket_status_response,
            content_type='application/json',
        )

        obj= codebase.Client(('example/alice', 'secret'))
        foo_proj = obj.projects['foo']
        result = len(foo_proj.statuses)

        self.assertEqual(result, 1)


class TicketPriorityTestCase(unittest.TestCase):
    @httpretty.activate
    def test_project_priorities_returns_map_of_priorities(self):
        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/projects',
            body=project_response,
            content_type='application/json',
        )

        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/foo/tickets/priorities',
            body=ticket_priority_response,
            content_type='application/json',
        )

        obj= codebase.Client(('example/alice', 'secret'))
        foo_proj = obj.projects['foo']
        priorities = list(foo_proj.priorities)

        self.assertEqual(len(priorities), 1)


class TicketTypeTestCase(unittest.TestCase):
    @httpretty.activate
    def test_project_types_returns_map_of_types(self):
        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/projects',
            body=project_response,
            content_type='application/json',
        )

        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/foo/tickets/types',
            body=ticket_type_response,
            content_type='application/json',
        )

        obj= codebase.Client(('example/alice', 'secret'))
        foo_proj = obj.projects['foo']
        types = list(foo_proj.types)

        self.assertEqual(len(types), 1)


class TicketCategoryTestCase(unittest.TestCase):
    @httpretty.activate
    def test_project_categories_returns_map_of_categories(self):
        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/projects',
            body=project_response,
            content_type='application/json',
        )

        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/foo/tickets/categories',
            body=ticket_category_response,
            content_type='application/json',
        )

        obj= codebase.Client(('example/alice', 'secret'))
        foo_proj = obj.projects['foo']
        categories = list(foo_proj.categories)

        self.assertEqual(len(categories), 1)
