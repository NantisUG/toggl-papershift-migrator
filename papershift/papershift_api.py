import requests


class PapershiftApiClient:

    default_params = {
        'base_url': 'https://app.papershift.com/public_api/v1'
    }

    def __init__(self, params):
        self.params = self.default_params.copy()
        self.params.update(params)

        self.base_url = self.params.get('base_url')
        self.token = self.params.get('token')
        self.workingarea_id = self.params.get('workingarea_id')
        self.location_id = self.params.get('location_id')
        self.user_id = self.params.get('user_id')

        return

    def create_time_entry(self, start, end, external_id):
        url = self.base_url + '/working_sessions'
        r = None
        try:
            r = requests.post(url, json={
                "api_token": self.token,
                "working_session": {
                    "location_id": self.location_id,
                    "working_area_id": self.workingarea_id,
                    "user_id": self.user_id,
                    "starts_at": start,
                    "ends_at": end,
                    "external_id": str(external_id)
                }
            })
        except ConnectionError as e:
            print(e)

        return r
