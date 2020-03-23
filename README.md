# PDdelete_by_tag

Delete stuff that has the given tag(s)

## Installation:

* Clone this repo and `cd` to it
* Create a virtual environment with Python 3: `python3 -m venv venv`
* Activate the virtual environment: `. venv/bin/activate`
* Get the dependencies: `pip install -r requirements.txt`

## Usage:

### Delete users, teams and escalation policies with tags "alice" and "bob":

`python ./delete_by_tag.py YOUR_PD_API_TOKEN alice,bob users,teams,escalation_policies`

### Sample Output:

```
Looking for tags... Found 2 tags.
  Looking for users with tag PXXXXXX...   Found 1 user
  Looking for teams with tag PXXXXXX...   Found 1 team
  Looking for escalation_policies with tag PXXXXXX...   Found 2 escalation_policies
  Looking for users with tag PXXXXXX...   Found 1 user
  Looking for teams with tag PXXXXXX...   Found 0 teams
  Looking for escalation_policies with tag PXXXXXX...   Found 0 escalation_policies

Found 2 objects to delete:
2 users:
  PXXXXXX
  PXXXXXX
1 team:
  PXXXXXX
2 escalation_policies:
  PXXXXXX
  PXXXXXX

Are you sure you want to delete? [y/N] y
OK, deleting...
Deleting escalation_policy PXXXXXX... Deleted.
Deleting escalation_policy PXXXXXX... Deleted.
Deleting team PXXXXXX... Deleted.
Deleting user PXXXXXX... Deleted.
Deleting user PXXXXXX... Deleted.

```
