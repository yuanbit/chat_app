I don't know of a module but this is fairly easy if you are using flask-login[1] and a cache with time-to-live, expiringdict[2].

from flask_login import Flask, login_required, current_user
from expiringdict import ExpiringDict

app = Flask(__name__)
current_sessions = ExpiringDict(max_age_seconds=60)

@app.request('/')
@login_required
def index():
    global current_sessions
    current_sessions[current_user.get_id()] = current_user

@app.request('/admin')
@admin_required
def show():
    global current_sessions
    # Do whatever you want with them
    for user_id in g.current_sessions:
        print user_id, current_sessions[user_id].email
You can make a decorator for updating the cache so your routes are less cluttered:

@app.request('/')
@login_required
@update_session # make sure this comes after login_required, one less check
def index():
    # Do whatever
The link you posted stores the users IP address. You can also do this here with a tuple if you need the remote address:

g.current_sessions[current_user.get_id()] = (current_user, request.remote_addr)
On logout, simply remove them from the list:

@app.request('/logout')
@login_required
def logout():
    global current_sessions
    current_sessions.pop(current_user.get_id())
https://flask-login.readthedocs.io/en/latest/

https://pypi.python.org/pypi/expiringdict/1.1.2
