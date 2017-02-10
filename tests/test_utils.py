import datetime
import unittest

from codebase import utils


class BuildTicketSearchQueryTestCase(unittest.TestCase):
    def test_no_params(self):
        result = utils.build_ticket_search_query()

        self.assertEqual(result, '')

    def test_single_param(self):
        result = utils.build_ticket_search_query(status='closed')

        self.assertEqual(result, 'status:"closed"')

    def test_combined_params(self):
        result = utils.build_ticket_search_query(status='closed', assignee='alice')

        self.assertEqual(result, 'assignee:"alice" status:"closed"')

    def test_multiple_values_for_param(self):
        result = utils.build_ticket_search_query(status=['in progress', 'closed'])

        self.assertEqual(result, 'status:"in progress","closed"')


class ParseDateTestCase(unittest.TestCase):
    def test_zulu_datetime(self):
        result = utils.parse_date('2016-01-02T03:04:05Z')
        expected = datetime.datetime(2016, 1, 2, 3, 4, 5, tzinfo=utils.utc)

        self.assertEqual(result, expected)

    def test_datetime_with_positive_fixed_offset(self):
        # The API can return these for Git commit timestamps.
        result = utils.parse_date('2016-01-02T03:04:05+01:30')
        # N.B. 1 hour earlier in UTC.
        expected = datetime.datetime(2016, 1, 2, 1, 34, 5, tzinfo=utils.utc)

        self.assertEqual(result, expected)

    def test_datetime_with_negative_fixed_offset(self):
        # The API can return these for Git commit timestamps.
        result = utils.parse_date('2016-01-02T03:04:05-01:30')
        # N.B. 1 hour earlier in UTC.
        expected = datetime.datetime(2016, 1, 2, 4, 34, 5, tzinfo=utils.utc)

        self.assertEqual(result, expected)

    def test_datetime_with_no_offset_returns_string(self):
        result = utils.parse_date('2016-01-02T03:04:05')

        self.assertEqual(result, '2016-01-02T03:04:05')

    def test_invalid_value_returns_the_value(self):
        result = utils.parse_date('foo')

        self.assertEqual(result, 'foo')

    def test_none_value_returns_none(self):
        result = utils.parse_date(None)

        self.assertIsNone(result)
