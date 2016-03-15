# Toggl to Papershift Migration Tool

The application fetches time entries from toggl and pushes them to papershift

## Execution

You will need several configuration items:

- toggl_api_token
- toggl_user_id
- toggl_workspace_id
- papershift_api_token
- papershift_location_id
- papershift_workingarea_id
- papershift_user_id

Additionally you can specify the time range as YYYY-MM-DD

It is safe to run the migration multiple times since the entries from toggl contain an id which is copied to papershift.
Duplicate items will not be created, also items overlapping other entries will cause an error.

Problems with the migration will be printed on the end of the program.

The program will spread the creation of the working sessions on papershift in multiple threads (more a programming exercise than a real performance problem) 

## Notes

If you are looking for a client supporting all commands see [toggl-cli by D. Robert Adams](https://github.com/drobertadams/toggl-cli/blob/master/toggl.py)