from csv import unregister_dialect
from msilib import MSIMODIFY_VALIDATE
from multiprocessing import allow_connection_pickling
from unittest.util import unorderable_list_difference
from flask import Flask, request, render_template, redirect, redirect, url_for, jsonify
from flask_login import LoginManager, login_required, UserMixin, current_user, login_user
from todo_app.mongodb_items import MongoDBTasks
from functools import wraps
from furl import furl
import flask_login
import requests
import json
import os




class ViewModel:

        def __init__(self, tasks):
            self._tasks = tasks

        @property
        def tasks(self):
            return self._tasks
            
        @property
        def to_do_items(self):
            to_do_output = []
            for item in self._tasks:
                if item.status == "To do":
                    to_do_output.append(item)
            return to_do_output

        @property
        def doing_items(self):
            doing_output = []
            for item in self._tasks:
                if item.status == "Doing":
                    doing_output.append(item)
            return doing_output
            
        @property
        def done_items(self):
            done_output = []
            for item in self._tasks:
                if item.status == "Done":
                    done_output.append(item)
            return done_output

class User(UserMixin):

    def __init__(self, id):
        self.id = id
        self.role = "Writer" if id == "7860342" else "Reader"
    
    
def create_app():
    
    app = Flask(__name__)
    mongodbtasks = MongoDBTasks()
    app.config.update(SECRET_KEY=os.urandom(24))

    client_id = os.environ.get('CLIENT_ID')
    client_secret= os.environ.get('CLIENT_SECRET')

    login_manager = LoginManager() 
    @login_manager.unauthorized_handler 
    # Redirect to the Github OAuth flow when unauthenticated 
    def unauthenticated(): 
        
        url = 'https://github.com/login/oauth/authorize'
        params = {
        'client_id': client_id,
        'redirect_uri': 'http://127.0.0.1:5000/login/callback',
        'state': 'unguessablerandomstring',
       
        }
       
        url = furl(url).set(params)
        return redirect(str(url), 302)

    @app.route('/login/callback')
    def oauth2_callback():
        # Login successful

        

        code = request.args.get('code')
        access_token_url = 'https://github.com/login/oauth/access_token'
        payload = {
            'client_id': client_id,
            'client_secret': client_secret,
            'code': code,
            'state': 'unguessablerandomstring'
        }
        # Obtain a temp access_token
        r = requests.post(access_token_url, json=payload, headers={'Accept': 'application/json'})
        access_token = json.loads(r.text).get('access_token')
        access_user_url = 'https://api.github.com/user'

        # Obtain user's data
        r = requests.get(access_user_url, headers={'Authorization': f'Bearer {access_token}'})
        # return jsonify({
        #     'status': 'success',
        #     'data': json.loads(r.text)
        # })
        #7860342
        user_id = json.loads(r.text)['id']
        print(user_id)

        login_user(user_id, remember=False, duration=None, force=False, fresh=True)
        items = mongodbtasks.get_all_tasks()
        item_view_model = ViewModel(items)
        return render_template('index.html',view_model=item_view_model)
        
        

    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id)

    
    login_manager.init_app(app) 

 
    def roles_accepted(*roles):
        def wrapper(fn):
            @wraps(fn)
            def decorated_view(*args, **kwargs):
                for role in roles:
                    if role != "Writer":
                        return oauth2_callback()
                        #it works but doesn't render the page properly
                return fn(*args, **kwargs)
            return decorated_view
        return wrapper
    

    
    @app.route('/')
    @login_required
    #@roles_accepted('Writer', 'Reader')
    def index():
        items = mongodbtasks.get_all_tasks()
        item_view_model = ViewModel(items)
        return render_template('index.html',view_model=item_view_model)
        
            
    @app.route('/add/add_item', methods=['GET', 'POST'])
    @login_required
    @roles_accepted('Writer')
    def add_to_do():
        mongodbtasks.add_task(title=request.form.get('item_name'))
        return oauth2_callback()


    @app.route('/remove/<id>', methods=['POST'])
    @login_required
    @roles_accepted('Writer')
    def delete_task(id):
        mongodbtasks.delete_task(id=request.form['remove_id'])
        return oauth2_callback()


    @app.route('/mark_complete/<id>', methods=['POST'])
    @login_required
    @roles_accepted('Writer')
    def mark_complete(id):
        mongodbtasks.mark_as_completed(id=request.form['complete_id'])
        return oauth2_callback()


    @app.route('/mark_doing/<id>', methods=['POST'])
    @login_required 
    @roles_accepted('Writer')
    def mark_doing(id):
        mongodbtasks.mark_as_doing(id=request.form['doing_id'])
        return oauth2_callback()


    @app.route('/mark_to_do/<id>', methods=['POST'])
    @login_required
    @roles_accepted('Writer')
    def mark_incomplete(id):
        mongodbtasks.mark_as_to_do(id=request.form['incomplete_id'])
        return oauth2_callback()
        

    app.config['LOGIN_DISABLED'] = os.getenv('LOGIN_DISABLED') == 'True'
    return app


if __name__ == "__main__":
    create_app.run(debug=True)


