from requests.auth import HTTPBasicAuth
import requests


# See: https://github.com/toggl/toggl_api_docs/blob/master/reports.md
# See: https://github.com/toggl/toggl_api_docs/blob/master/reports/detailed.md
class TogglReportsApiClient:

    default_params = {
        'token': '',
        'base_url': 'https://toggl.com/reports/api/v2',
        'user_agent': 'Papershift Migration maeckle@nantis.de'
    }

    def __init__(self, params):
        self.params = self.default_params.copy()
        self.params.update(params)

        self.base_url = self.params.get('base_url')
        self.user_agent = self.params.get('user_agent')
        self.wid = self.params.get('wid')
        self.user_id = self.params.get('user_id')
        self.auth = self.__get_basic_auth(self.params.get('token'))
        return

    @staticmethod
    def __get_basic_auth(token):
        return HTTPBasicAuth(token, 'api_token')

    def get_details(self, page, start, end):
        url = self.base_url + '/details'
        r = None
        try:
            r = requests.get(url, auth=self.auth, params={
                'workspace_id': self.wid,
                'user_agent': self.user_agent,
                'page': page,
                'since': start,
                'until': end,
                'user_ids': self.user_id
            })
        except ConnectionError as e:
            print(e)

        return r
