from requests.auth import HTTPBasicAuth
import requests


class TogglApiClient:

    default_params = {
        'token': '',
        'base_url': 'https://www.toggl.com/api/v8',
        'app_name': 'Papershift Migration'
    }

    errorCodes = {
        402: 'Payment required - feature not included in current subscription',
        410: 'Gone - API deprecated',
        429: 'Too many requests'
    }

    def __init__(self, params):
        self.params = self.default_params.copy()
        self.params.update(params)

        self.base_url = self.params.get('base_url')
        self.app_name = self.params.get('app_name')
        self.wid = self.params.get('wid')
        self.auth = self.__get_basic_auth(self.params.get('token'))
        return

    @staticmethod
    def __get_basic_auth(token):
        return HTTPBasicAuth(token, 'api_token')

    def get_current_time_entry(self):
        url = self.base_url + '/time_entries/current'
        r = None
        try:
            r = requests.get(url, auth=self.auth)
            print(r)
        except ConnectionError as e:
            print(e)

        return r

    def start_time_entry(self, description):
        url = self.base_url + '/time_entries/start'
        r = None
        try:
            r = requests.post(url, auth=self.auth, json={
                'time_entry': {
                    'description': description,
                    'created_with': self.app_name,
                    'wid': self.wid
                }
            })
            print(r)
        except ConnectionError as e:
            print(e)

        return r

    def stop_time_entry(self, entry_id):
        r = None
        url = self.base_url + '/time_entries/' + str(entry_id) + '/stop'
        try:
            r = requests.put(url, auth=self.auth)
            print(r)
        except ConnectionError as e:
            print(e)
        return r
