# 2020-09-10 17:57:54 -0400 - Jeremy Axmacher - Add readme - lines:,2,3,4,5,6,7,8,9,10,11,12
# Installation instructions

 * Clone this repo and change into the `tasker` folder
 * `python3 -m venv venv`
 * `source venv/bin/activate` or, for windows `venv\bin\activate.bat`
 * `pip install -r requirements.txt`
 * `flask create-db`
 * `flask run`
 * Open http://localhost:5000 in a browser

That should show a simple form and when you submit entries, a list of the recorded entries.
