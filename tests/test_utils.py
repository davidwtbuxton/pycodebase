import unittest

from codebase.utils import build_ticket_search_query


class BuildTicketSearchQueryTestCase(unittest.TestCase):
    def test_no_params(self):
        result = build_ticket_search_query()

        self.assertEqual(result, '')

    def test_single_param(self):
        result = build_ticket_search_query(status='closed')

        self.assertEqual(result, 'status:"closed"')

    def test_combined_params(self):
        result = build_ticket_search_query(status='closed', assignee='alice')

        self.assertEqual(result, 'assignee:"alice" status:"closed"')

    def test_multiple_values_for_param(self):
        result = build_ticket_search_query(status=['in progress', 'closed'])

        self.assertEqual(result, 'status:"in progress","closed"')
