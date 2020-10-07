# 2020-09-10 17:57:54 -0400 - Jeremy Axmacher - Add readme - lines:,5,6,7,8,9,10,13,14,15
# 2020-09-23 21:27:33 -0400 - Jeremy Axmacher - Reorganize file tree - lines:,11
# 2020-09-23 23:14:46 -0400 - J Axmacher - Update readme.md - lines:,12
# 2020-09-23 23:33:53 -0400 - J Axmacher - Add example for creating user interactively for testing - lines:,16,17,18,19,20,21,22,23,24,25,26,27,28,29
# Installation instructions

 * Clone this repo and change into the `tasker` folder
 * `python3 -m venv venv`
 * `source venv/bin/activate` or, for windows `venv\bin\activate.bat`
 * `pip install -r requirements.txt`
 * `export FLASK_APP=tasker`
 * `flask create-db`
 * `flask run`
 * Open http://localhost:5000 in a browser

That should show a simple form and when you submit entries, a list of the recorded entries.

How to create a user interactively for testing:

`flask shell`

```
from tasker import create_app
app = create_app()
ctx = app.test_request_context()
ctx.push()
from tasker.models import User
User.create_user('test@email.com', 'password', 'America/New_York')
```
