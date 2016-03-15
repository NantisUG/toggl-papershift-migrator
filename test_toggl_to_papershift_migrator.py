import unittest
import requests_mock
from toggl_to_papershift_migrator import TogglToPapershiftMigrator


class TogglToPapershiftMigratorTest(unittest.TestCase):
    def testMigrate(self):
        with requests_mock.mock() as m:
            m.get('https://toggl.com/reports/api/v2/details', json={
                "total_count": 6,
                "per_page": 50,
                "data": [
                    {
                        "id": 123456,
                        "uid": 123,
                        "description": "Office",
                        "start": "2016-02-04T13:00:00+01:00",
                        "end": "2016-02-04T18:30:00+01:00"
                    },
                    {
                        "id": 123456,
                        "uid": 123,
                        "description": "Office",
                        "start": "2016-02-04T13:00:00+01:00",
                        "end": "2016-02-04T18:30:00+01:00"
                    }
                ]
            })

            m.post('https://app.papershift.com/public_api/v1/working_sessions', json={'data': 'test'})

            migrator = TogglToPapershiftMigrator(params={
                'toggl_api_token': 'tl123',
                'toggl_user_id': 123,
                'toggl_workspace_id': 123,
                'papershift_api_token': 'ps123',
                'papershift_location_id': 123,
                'papershift_workingarea_id': 123,
                'papershift_user_id': 123
            })

            migrator.migrate('2016-01-01', '2016-12-31')

            # The mock should be called 3 times since it takes 3 requests to fetch all data
            self.assertEqual(m.call_count, 9)

            entry_queue = migrator.get_entries_queue()
            self.assertEqual(entry_queue.qsize(), 0)
