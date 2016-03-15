import unittest
import requests_mock
from toggl.toggl_reports_api import TogglReportsApiClient


class TogglReportsApiClientTest(unittest.TestCase):

    def testGetDetails(self):

        with requests_mock.mock() as m:

            m.get('https://toggl.com/reports/api/v2/details', json={'data': 'test'})
            toggl_client = TogglReportsApiClient({
                'wid': '12345',
                'token': 'TOKEN123'
            })

            result = toggl_client.get_details(1, '2016-01-01', '2016-12-01')

            history = m.request_history[0]

            self.assertEqual(m.called, True)
            self.assertEqual(result.status_code, 200)

            self.assertEqual(history.qs['workspace_id'], ['12345'])
            self.assertEqual(history.qs['since'], ['2016-01-01'])
            self.assertEqual(history.qs['until'], ['2016-12-01'])
            self.assertEqual(history.qs['user_agent'], ['papershift migration maeckle@nantis.de'])

            self.assertEqual(result.json().get('data'), 'test')
