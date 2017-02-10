# encoding: utf-8
import json
import unittest

import httpretty

import codebase
import fixtures


class ProjectTestCase(unittest.TestCase):
    @httpretty.activate
    def test_projects_returns_map_of_projects(self):
        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/projects',
            body=fixtures.project_response,
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
            body=fixtures.project_response,
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
            body=fixtures.project_response,
            content_type='application/json',
        )

        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/foo/assignments',
            body=fixtures.project_user_response,
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
            body=fixtures.project_response,
            content_type='application/json',
        )

        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/foo/tickets',
            responses=[
                httpretty.Response(body=fixtures.ticket_response, status=200, content_type='application/json'),
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
            body=fixtures.project_response,
            content_type='application/json',
        )

        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/foo/tickets',
            responses=[
                httpretty.Response(body=fixtures.ticket_response, status=200, content_type='application/json'),
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
            body=fixtures.project_response,
            content_type='application/json',
        )

        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/foo/tickets',
            responses=[
                httpretty.Response(body=fixtures.ticket_response, status=200, content_type='application/json'),
                httpretty.Response(body=json.dumps([]), status=404, content_type='application/json'),
            ],
        )

        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/foo/tickets/123/notes',
            body=fixtures.ticket_note_response,
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
            body=fixtures.project_response,
            content_type='application/json',
        )

        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/foo/repositories',
            body=fixtures.repository_response,
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
            body=fixtures.project_response,
            content_type='application/json',
        )

        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/foo/repositories',
            body=fixtures.repository_response,
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
            body=fixtures.project_response,
            content_type='application/json',
        )

        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/foo/repositories',
            body=fixtures.repository_response,
            content_type='application/json',
        )

        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/foo/foo-code-repo/deployments',
            responses=[
                httpretty.Response(body=fixtures.deployment_response, content_type='application/json'),
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
            body=fixtures.project_response,
            content_type='application/json',
        )

        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/foo/tickets/statuses',
            body=fixtures.ticket_status_response,
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
            body=fixtures.project_response,
            content_type='application/json',
        )

        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/foo/tickets/priorities',
            body=fixtures.ticket_priority_response,
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
            body=fixtures.project_response,
            content_type='application/json',
        )

        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/foo/tickets/types',
            body=fixtures.ticket_type_response,
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
            body=fixtures.project_response,
            content_type='application/json',
        )

        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/foo/tickets/categories',
            body=fixtures.ticket_category_response,
            content_type='application/json',
        )

        obj= codebase.Client(('example/alice', 'secret'))
        foo_proj = obj.projects['foo']
        categories = list(foo_proj.categories)

        self.assertEqual(len(categories), 1)
