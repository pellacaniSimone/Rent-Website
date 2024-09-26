# RENT

admin simone
Email note@type.io
password paperinik88


# 3 users with permissions
- randomuser01: registered but not confirmed
- randomuser02: registered and confirmed
- randomuser03: owner user (recommended user)

## password
Valid for each randomuser0`x`
- 123user123


# init

Do not use `init.sh` unless you need to rebuild the entire database, it's normally not necessary.
Afterward, call init_db, a dummy maintenance page, if needed.

# usage
- Normal user usage via randomuser02 allows searching, booking, and viewing history.

- Pro user usage is available via randomuser03, who can add properties, check appointments, and view the performance of their rental properties.

- Staff usage with user simone can confirm pro users and add new market zones to operate in.

- randomuser01 is used for user confirmation, typically through a confirmation email in a real scenario. In this educational case, a page with a confirmation button is displayed. Once confirmed, the user becomes a common user like randomuser02. It's not possible to revert to an unregistered user, this is a destructive test.

# setup (Linux shell commands)
To install, create your own virtual environment with:
- `python venv venv-django`
Activate the newly created virtual environment:
- `source venv-django/bin/activate`
Install the required packages:
- `pip install -r requirements.txt`
Run django

# compatibility

To check the Python version being used, refer to the `.python-version` file for pyenv compliance.
