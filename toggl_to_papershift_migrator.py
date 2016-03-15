import time

from toggl.toggl_reports_api import TogglReportsApiClient
from papershift.papershift_api import PapershiftApiClient

import threading
import queue


class PapershiftThread(threading.Thread):

    def __init__(self, thread_id, stop_threads, q, eq, client):
        super(PapershiftThread, self).__init__()
        self.thread_id = thread_id
        self.stop_thread = stop_threads
        self.q = q
        self.eq = eq
        # The requests class is thread safe, so we pass it in directly
        self.client = client

    def put_data(self, data):
        res = self.client.create_time_entry(data['start'], data['end'], data['id'])
        return res

    def put_time_entry(self, data):

        result = self.put_data(data)

        if result is not None:
            if result.status_code is not 200:
                # Put the failed entries in an error queue
                data['error_text'] = result.text
                data['error_code'] = result.status_code
                self.eq.put(data)

        self.q.task_done()

    def run(self):

        while not self.stop_thread.is_set():
            try:
                entry = self.q.get(True, 1)
                self.put_time_entry(entry)
            except queue.Empty:
                pass


# Migrate time entries from toggl to papershift
class TogglToPapershiftMigrator:

    default_params = {
        'toggl_requests_per_second': 1
    }

    toggl_client = None
    papershift_client = None

    def __init__(self, params):
        self.params = self.default_params.copy()
        self.params.update(params)

        self.toggl_api_token = self.params.get('toggl_api_token')
        self.toggl_user_id = self.params.get('toggl_user_id')
        self.toggl_workspace_id = self.params.get('toggl_workspace_id')

        self.papershift_api_token = self.params.get('papershift_api_token')
        self.papershift_location_id = self.params.get('papershift_location_id')
        self.papershift_workingarea_id = self.params.get('papershift_workingarea_id')
        self.papershift_user_id = self.params.get('papershift_user_id')

        # A queue, where we will put all time entries fetched from toggl
        self.time_entries = queue.Queue()
        self.error_entries = queue.Queue()
        self.stop_threads = threading.Event()

        self.threads = []

        self.toggl_client = TogglReportsApiClient({
            'token': self.toggl_api_token,
            'wid': self.toggl_workspace_id,
            'user_id': self.toggl_user_id
        })

        self.papershift_client = PapershiftApiClient({
            'token': self.papershift_api_token,
            'location_id': self.papershift_location_id,
            'workingarea_id': self.papershift_workingarea_id,
            'user_id': self.papershift_user_id
        })

    def get_entries_queue(self):
        return self.time_entries

    def get_is_running(self):
        return not self.stop_threads.is_set()

    def put_entries(self, entries):
        if entries:
            for entry in entries:
                self.time_entries.put(entry)

    def create_worker_threads(self, number):
        for n in range(0, number):

            thread = PapershiftThread(
                n,
                self.stop_threads,
                self.time_entries,
                self.error_entries,
                self.papershift_client
            )

            thread.start()
            self.threads.append(thread)

    def migrate(self, start, end):
        page = 1
        result = self.toggl_client.get_details(page, start, end)

        if result is not None and result.status_code is 200:
            entries = result.json().get('data')
            self.put_entries(entries)

            total_items = result.json().get('total_count')
            counter = len(entries)

            # Multi-threaded creation
            self.create_worker_threads(5)

            # If there is more data fetch it
            while counter < total_items:
                # Slow down the api, since toggl allows only 1 req / s
                time.sleep(self.params.get('toggl_requests_per_second'))
                page += 1
                result = self.toggl_client.get_details(page, start, end)
                entries = result.json().get('data')
                counter += len(entries)
                self.put_entries(entries)

            # Wait for all work to be done on the queue
            self.time_entries.join()

            # End all threads
            self.stop_threads.set()

            # Wait until threads are finished
            for thread in self.threads:
                thread.join()

            while not self.error_entries.empty():
                error = self.error_entries.get()
                print(
                    'Error in the following toggl entry:', str(error['id']),
                    'from', str(error['start']),
                    'to', str(error['end']),
                    'with error', str(error['error_code']),
                    'and message', str(error['error_text'])
                )
                self.error_entries.task_done()

            self.error_entries.join()
