from toggl_to_papershift_migrator import TogglToPapershiftMigrator


class Migrator:

    @staticmethod
    def main():

        print('Welcome to the the toggl to papershift migration tool')
        print('----------------------------------------------------------------------------------')
        print('You will need to migrate your users one by one.')
        print('You can run the migration multiple times since the entries contain an external id.')
        print('----------------------------------------------------------------------------------')

        # Get toggl stuff
        toggl_api_key = input('Input the toggl API Key: ')
        toggl_workspace_id = input('Input the toggl Workspace ID: ')
        toggl_user_id = input('Input the toggl user id: ')

        # Get papershift stuff
        papershift_api_key = input('Input the papershift api key: ')
        papershift_location_id = input('Input the papershift location id: ')
        papershift_workingarea_id = input('Input the papershift workingarea id: ')
        papershift_user_id = input('Input the papershift user id: ')

        # Get time stuff
        start = input('Input the Starting date of the migration (YYYY-MM-DD): ')
        end = input('Input the Ending date of the migration (YYYY-MM-DD): ')

        migrator = TogglToPapershiftMigrator(params={
            'toggl_api_token': str(toggl_api_key),
            'toggl_user_id': int(toggl_user_id),
            'toggl_workspace_id': int(toggl_workspace_id),
            'papershift_api_token': str(papershift_api_key),
            'papershift_location_id': int(papershift_location_id),
            'papershift_workingarea_id': int(papershift_workingarea_id),
            'papershift_user_id': int(papershift_user_id)
        })

        migrator.migrate(str(start), str(end))

        print('Thank you for using the migrator, all jobs are done.')


if __name__ == '__main__':
    Migrator().main()
