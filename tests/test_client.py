# encoding: utf-8
import datetime
import json
import os
import tempfile
import types
import unittest

import httpretty

import codebase
import fixtures


class ClientTestCase(unittest.TestCase):
    def test_client_properties(self):
        obj = codebase.Client(('example/alice', 'secret'))

        obj.add_my_key
        obj.add_user_key
        obj.create_deployment
        obj.create_milestone
        obj.create_ticket
        obj.create_ticket_note
        obj.get_activity
        obj.get_commits
        obj.get_deployments
        obj.get_file_contents
        obj.get_milestones
        obj.get_my_keys
        obj.get_project_activity
        obj.get_projects
        obj.get_repositories
        obj.get_ticket_categories
        obj.get_ticket_notes
        obj.get_ticket_priorities
        obj.get_ticket_statuses
        obj.get_ticket_types
        obj.get_tickets
        obj.get_user_keys
        obj.reset_cache
        obj.update_milestone

    @httpretty.activate
    def test_get_projects_returns_generator_of_projects(self):
        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/projects',
            body=fixtures.project_response,
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
                httpretty.Response(body=fixtures.activity_response, content_type='application/json'),
                httpretty.Response(body=json.dumps([]), content_type='application/json'),
            ],
        )

        obj = codebase.Client(('example/alice', 'secret'))
        result = obj.get_project_activity('foo')

        self.assertIsInstance(result, types.GeneratorType)

        activities = list(result)

        self.assertEqual(len(activities), 1)
        self.assertEqual(activities[0]['actor_name'], u'Alice A')

    @httpretty.activate
    def test_get_account_activity_returns_generator_of_activity(self):
        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/activity',
            responses=[
                httpretty.Response(body=fixtures.activity_response, content_type='application/json'),
                httpretty.Response(body=json.dumps([]), content_type='application/json'),
            ],
        )

        obj = codebase.Client(('example/alice', 'secret'))
        result = obj.get_activity()

        self.assertIsInstance(result, types.GeneratorType)

        activities = list(result)

        self.assertEqual(len(activities), 1)
        self.assertEqual(activities[0]['actor_name'], u'Alice A')

    def test_create_new_client_from_secrets_file(self):
        with tempfile.NamedTemporaryFile(delete=False) as fh:
            filename = fh.name
            fh.write('[api]\nusername = example/alice\nkey = secret\n')

        try:
            client = codebase.Client.with_secrets(filename)
        finally:
            os.unlink(filename)

        self.assertEqual(client.auth, ('example/alice', 'secret'))


class TicketsTestCase(unittest.TestCase):
    @httpretty.activate
    def test_get_tickets(self):
        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/foo/tickets',
            responses=[
                httpretty.Response(body=fixtures.ticket_response, content_type='application/json'),
                httpretty.Response(body='[]', content_type='application/json', status=404),
            ],
        )

        obj = codebase.Client(('example/alice', 'secret'))
        result = obj.get_tickets('foo')
        tickets = list(result)

        self.assertIsInstance(result, types.GeneratorType)
        self.assertEqual(len(tickets), 1)

    @httpretty.activate
    def test_create_ticket_with_assignee_name(self):
        users_data = [
            {
                'user': {
                    'username': 'alice',
                    'id': 999,
                    'email_addresses': ['alice@example.com'],
                },
            },
        ]

        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/foo/assignments',
            body=json.dumps(users_data),
            content_type='application/json',
        )
        httpretty.register_uri(
            httpretty.POST,
            'https://api3.codebasehq.com/foo/tickets',
            body=json.dumps({}),
            content_type='application/json',
        )

        obj = codebase.Client(('example/alice', 'secret'))
        obj.create_ticket('foo', summary='Summary', assignee='alice')

        request = httpretty.last_request()
        body = json.loads(request.body)

        # The name was converted to the user ID.
        self.assertEqual(body['ticket']['assignee_id'], 999)


class PublicKeysTestCase(unittest.TestCase):
    @httpretty.activate
    def test_get_user_keys(self):
        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/users/bob/public_keys',
            body=fixtures.public_keys_response,
            content_type='application/json',
        )

        obj = codebase.Client(('example/alice', 'secret'))
        result = list(obj.get_user_keys('bob'))

        self.assertEqual(len(result), 1)
        self.assertEqual(
            result[0],
            {
                u'description': u'Regular key',
                u'key': u'ssh-rsa abc==',
            },
        )

    @httpretty.activate
    def test_get_my_keys(self):
        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/users/carol/public_keys',
            body=fixtures.public_keys_response,
            content_type='application/json',
        )

        # The username is derived from the auth username.
        obj = codebase.Client(('example/carol', 'secret'))
        result = list(obj.get_my_keys())

        self.assertEqual(len(result), 1)
        self.assertEqual(
            result[0],
            {
                u'description': u'Regular key',
                u'key': u'ssh-rsa abc==',
            },
        )

    @httpretty.activate
    def test_add_user_key(self):
        httpretty.register_uri(
            httpretty.POST,
            'https://api3.codebasehq.com/users/carol/public_keys',
            body='{}',
            content_type='application/json',
        )

        obj = codebase.Client(('example/carol', 'secret'))
        obj.add_user_key('carol', 'New key', 'ssh-rsa ABCD1234')

        request = httpretty.last_request()

        self.assertEqual(request.method, 'POST')
        self.assertEqual(request.path, '/users/carol/public_keys')
        self.assertEqual(
            json.loads(request.body),
            {
                'public_key': {
                    'description': 'New key',
                    'key': 'ssh-rsa ABCD1234',
                },
            },
        )


class CommitsTestCase(unittest.TestCase):
    @httpretty.activate
    def test_get_commits(self):
        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/foo/bar/commits/master',
            responses=[
                httpretty.Response(body=fixtures.commit_response, content_type='application/json'),
                httpretty.Response(body=json.dumps([]), content_type='application/json'),
            ],
        )

        obj = codebase.Client(('example/alice', 'secret'))
        result = obj.get_commits(project='foo', repo='bar', ref='master')

        self.assertIsInstance(result, types.GeneratorType)

        commits = list(result)

        self.assertEqual(len(commits), 1)
        self.assertEqual(commits[0]['committer_name'], u'Alice A')


class MilestonesTestCase(unittest.TestCase):
    @httpretty.activate
    def test_get_milestones(self):
        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/foo/milestones',
            responses=[
                httpretty.Response(body=fixtures.milestones_response, content_type='application/json'),
            ],
        )

        obj = codebase.Client(('example/alice', 'secret'))
        result = obj.get_milestones(project='foo')

        self.assertIsInstance(result, types.GeneratorType)

        milestones = list(result)

        self.assertEqual(len(milestones), 1)
        self.assertEqual(
            milestones[0],
            {
                'deadline': None,
                'description': u'',
                'estimated_time': 0,
                'id': 123,
                'identifier': u'123-4-5-6-uuid',
                'name': u'Bar milestone',
                'parent_id': None,
                'responsible_user_id': 987,
                'start_at': None,
                'status': u'active',
            },
        )

    @httpretty.activate
    def test_create_milestone(self):
        httpretty.register_uri(
            httpretty.POST,
            'https://api3.codebasehq.com/foo/milestones',
            body=json.dumps({}),
            content_type='application/json',
        )

        obj = codebase.Client(('example/alice', 'secret'))
        result = obj.create_milestone('foo', 'NameOfMilestone')

        self.assertEqual(result, {})

    @httpretty.activate
    def test_update_milestone(self):
        httpretty.register_uri(
            httpretty.PUT,
            'https://api3.codebasehq.com/foo/milestones/123',
            body=json.dumps({}),
            content_type='application/json',
        )

        xmas = datetime.date(1999, 12, 31)
        obj = codebase.Client(('example/alice', 'secret'))
        result = obj.update_milestone('foo', 123, start_at=xmas, deadline=xmas)

        self.assertEqual(result, {})


class TicketTypesTestCase(unittest.TestCase):
    @httpretty.activate
    def test_get_ticket_types(self):
        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/foo/tickets/types',
            body=fixtures.ticket_type_response,
            content_type='application/json',
        )

        obj= codebase.Client(('example/alice', 'secret'))
        result = obj.get_ticket_types('foo')
        ticket_types = list(result)

        self.assertIsInstance(result, types.GeneratorType)
        self.assertEqual(len(ticket_types), 1)


class TicketCategoriesTestCase(unittest.TestCase):
    @httpretty.activate
    def test_get_ticket_categories(self):
        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/foo/tickets/categories',
            body=fixtures.ticket_category_response,
            content_type='application/json',
        )

        obj= codebase.Client(('example/alice', 'secret'))
        result = obj.get_ticket_categories('foo')
        categories = list(result)

        self.assertIsInstance(result, types.GeneratorType)
        self.assertEqual(len(categories), 1)


class TicketPrioritiesTestCase(unittest.TestCase):
    @httpretty.activate
    def test_get_ticket_priorities(self):
        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/foo/tickets/priorities',
            body=fixtures.ticket_priority_response,
            content_type='application/json',
        )

        obj= codebase.Client(('example/alice', 'secret'))
        result = obj.get_ticket_priorities('foo')
        priorities = list(result)

        self.assertIsInstance(result, types.GeneratorType)
        self.assertEqual(len(priorities), 1)


class TicketStatusesTestCase(unittest.TestCase):
    @httpretty.activate
    def test_get_ticket_statuses(self):
        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/foo/tickets/statuses',
            body=fixtures.ticket_status_response,
            content_type='application/json',
        )

        obj= codebase.Client(('example/alice', 'secret'))
        result = obj.get_ticket_statuses('foo')
        statuses = list(result)

        self.assertIsInstance(result, types.GeneratorType)
        self.assertEqual(len(statuses), 1)


class TicketNotesTestCase(unittest.TestCase):
    @httpretty.activate
    def test_get_ticket_notes(self):
        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/foo/tickets/123/notes',
            body=fixtures.ticket_note_response,
            content_type='application/json',
        )

        obj= codebase.Client(('example/alice', 'secret'))
        result = obj.get_ticket_notes('foo', 123)
        ticket_notes = list(result)

        self.assertIsInstance(result, types.GeneratorType)
        self.assertEqual(len(ticket_notes), 1)

    @httpretty.activate
    def test_create_ticket_note(self):
        httpretty.register_uri(
            httpretty.POST,
            'https://api3.codebasehq.com/foo/tickets/123/notes',
            body='{}',
            content_type='application/json',
        )

        obj= codebase.Client(('example/alice', 'secret'))
        obj.create_ticket_note('foo', 123, content='New note')
        request = httpretty.last_request()

        self.assertEqual(request.path, '/foo/tickets/123/notes')
        self.assertEqual(request.method, 'POST')
        self.assertEqual(
            json.loads(request.body),
            {
                'ticket_note': {'content': 'New note'},
            },
        )


class DeploymentsTestCase(unittest.TestCase):
    @httpretty.activate
    def test_get_deployments(self):
        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/foo/foo-code-repo/deployments',
            responses=[
                httpretty.Response(body=fixtures.deployment_response, content_type='application/json'),
                httpretty.Response(body=json.dumps([]), content_type='application/json', status=404),
            ],
        )

        obj= codebase.Client(('example/alice', 'secret'))
        result = obj.get_deployments('foo', 'foo-code-repo')
        deployments = list(result)

        self.assertIsInstance(result, types.GeneratorType)
        self.assertEqual(len(deployments), 1)

    @httpretty.activate
    def test_create_deployment(self):
        httpretty.register_uri(
            httpretty.POST,
            'https://api3.codebasehq.com/foo/foo-code-repo/deployments',
            body='{}',
            content_type='application/json',
        )

        obj= codebase.Client(('example/alice', 'secret'))
        result = obj.create_deployment('foo', 'foo-code-repo', 'master', 'v1',
            'live', 'example.com')

        request = httpretty.last_request()

        self.assertEqual(request.method, 'POST')
        self.assertEqual(request.path, u'/foo/foo-code-repo/deployments')
        self.assertEqual(
            json.loads(request.body),
            {
                'deployment': {
                    'branch': 'master',
                    'environment': 'live',
                    'revision': 'v1',
                    'servers': 'example.com',
                },
            }
        )


class RepositoriesTestCase(unittest.TestCase):
    @httpretty.activate
    def test_get_repositories(self):
        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/foo/repositories',
            body=fixtures.repository_response,
            content_type='application/json',
        )

        obj= codebase.Client(('example/alice', 'secret'))
        result = obj.get_repositories('foo')
        repositories = list(result)

        self.assertIsInstance(result, types.GeneratorType)
        self.assertEqual(len(repositories), 1)


class ProjectUsersTestCase(unittest.TestCase):
    @httpretty.activate
    def test_get_project_users(self):
        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/foo/assignments',
            body=fixtures.project_user_response,
            content_type='application/json',
        )

        obj= codebase.Client(('example/alice', 'secret'))
        result = obj.get_project_users('foo')
        users = list(result)

        self.assertIsInstance(result, types.GeneratorType)
        self.assertEqual(len(users), 1)


class ProjectsTestCase(unittest.TestCase):
    @httpretty.activate
    def test_get_projects(self):
        httpretty.register_uri(
            httpretty.GET,
            'https://api3.codebasehq.com/projects',
            body=fixtures.project_response,
            content_type='application/json',
        )

        obj= codebase.Client(('example/alice', 'secret'))
        result = obj.get_projects()
        projects = list(result)

        self.assertIsInstance(result, types.GeneratorType)
        self.assertEqual(len(projects), 1)


class UploadFilesTestCase(unittest.TestCase):
    @httpretty.activate
    def test_upload_files(self):
        httpretty.register_uri(
            httpretty.POST,
            'https://api3.codebasehq.com/uploads',
            body=fixtures.file_uploads_response,
            content_type='application/json',
        )
        obj= codebase.Client(('example/alice', 'secret'))

        # You upload a list of (file-name, file data) pairs.
        files = [('foo.gif', 'GIF89a??')]
        result = obj.upload_files(files)
        uploads = list(result)

        request = httpretty.last_request()

        self.assertIsInstance(result, types.GeneratorType)
        self.assertEqual(len(uploads), 1)
        self.assertEqual(request.method, 'POST')
        self.assertEqual(request.path, '/uploads')
        self.assertEqual(request.headers['Content-type'][:20], 'multipart/form-data;')
