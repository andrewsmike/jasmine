Jasmine Backlog Prioritizer
===========================

Updates the jasmine tracker google sheet with task and story priority calculations.
These calculations allow tasks to be prioritized appropriately, even when they have no direct value themselves.

Usage
=====
There are some packages required for this tool.
You'll have to figure them out yourself.
These may be helpful:
- https://developers.google.com/sheets/api/quickstart/python

I used this:
- `pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib oauth2client`



Place an appropriate oauth2 token in the `credentials.json` file.
You may create new app credentials or just copy the ones from another dev.
Enter the directory and run `python update_backlog.py`, follow the auth flow, and it should update the Jasmine Tracker document automatically.


Priority Calculation
====================
Stories are defined as being an end-goal; they have cost, they may depend on tasks (but not other stories), and they have value.
Tasks have no inherent value, may depend on other tasks, and have cost.
The priority of a story is approximately `value / minimum_required_cost`.
The priority of a task is the aggregate value and effort for the _best_ subset of all descendent stories.
The end result is that tasks blocking multiple stories end up with a high priority, as you would expect, and necessarily have priority greater than or equal to any downstream stories.


