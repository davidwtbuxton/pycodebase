# encoding: utf-8
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

        obj.projects
        obj.create_deployment
        obj.create_ticket
        obj.create_ticket_note
        obj.get_activity
        obj.get_commits
        obj.get_deployments
        obj.get_file_contents
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
        obj.get_my_keys
        obj.add_user_key
        obj.add_my_key

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
