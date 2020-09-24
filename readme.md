# Installation instructions

 * Clone this repo and change into the `tasker` folder
 * `python3 -m venv venv`
 * `source venv/bin/activate` or, for windows `venv\\bin\\activate.bat`
 * `pip install -r requirements.txt`
 * `export FLASK_APP=tasker`
 * `flask create-db`
 * `flask run`
 * Open http://localhost:5000 in a browser

That should show a simple form and when you submit entries, a list of the recorded entries. Test.
