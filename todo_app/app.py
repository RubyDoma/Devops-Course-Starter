from flask import Flask, request, render_template, redirect, redirect, jsonify, url_for
from flask_login import LoginManager, login_required, UserMixin, AnonymousUserMixin, current_user, login_user 
from todo_app.mongodb_items import MongoDBTasks
from functools import wraps
from furl import furl
import requests
import json
import os

from loggly.handlers import HTTPSHandler
from logging import Formatter


import logging


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
        self.role = "Writer" if id == "78603420" else "Reader"
        self.roles = ["Reader", "Writer"]

class AnonymousUser(AnonymousUserMixin):
    
    def __init__(self):
        self.role = "Reader"


def create_app():
    
    app = Flask(__name__)
    mongodbtasks = MongoDBTasks()
    app.config.update(SECRET_KEY=os.environ.get('SECRET_KEY'))
    app.logger.setLevel(os.environ.get('LOG_LEVEL'))
   

    client_id = os.environ.get('CLIENT_ID')
    client_secret= os.environ.get('CLIENT_SECRET')
    redirect_uri= os.environ.get('REDIRECT_URI')

    login_manager = LoginManager() 
    login_manager.anonymous_user = AnonymousUser

    if os.environ.get('LOGGLY_TOKEN') is not None:
        handler = HTTPSHandler(f'https://logs-01.loggly.com/inputs/{os.environ.get("LOGGLY_TOKEN")}/tag/todo-app')
        print(os.environ.get('LOGGLY_TOKEN'))
        handler.setFormatter(Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
        )
        app.logger.addHandler(handler)

    @login_manager.unauthorized_handler 
    # Redirect to the Github OAuth flow when unauthenticated 
    def unauthenticated(): 
        
        url = 'https://github.com/login/oauth/authorize'
        params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
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
        if r.status_code != 200:
            app.logger.info(f'issue when obtaining access token')
        access_token = json.loads(r.text).get('access_token')
        access_user_url = 'https://api.github.com/user'

        # Obtain user's data
        r = requests.get(access_user_url, headers={'Authorization': f'Bearer {access_token}'})
        # return jsonify({
        #     'status': 'success',
        #     'data': json.loads(r.text)
        # })


        user_id = json.loads(r.text).get("id")
        user = User(user_id)

        login_user(user)
        app.logger.info(f'user with id {user_id} logged in successfully')
        

        return redirect(url_for('index'))
    
    

    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id)

    
    login_manager.init_app(app) 


 
    def roles_accepted(*roles):
        def wrapper(fn):
            @wraps(fn)
            def decorated_view(*args, **kwargs):
                for role in roles:
                    if role == current_user.role:
                        return fn(*args, **kwargs)
                return "you don't have permission"
            return decorated_view
        return wrapper
    

    
    @app.route('/')
    @login_required
    @roles_accepted('Writer', 'Reader')
    def index():
        items = mongodbtasks.get_all_tasks()
        item_view_model = ViewModel(items)
        return render_template('index.html',view_model=item_view_model, current_user = current_user)
        
            
    @app.route('/add/add_item', methods=['GET', 'POST'])
    @login_required
    @roles_accepted('Writer')
    def add_to_do():
        name = request.form.get('item_name')
        mongodbtasks.add_task(title=request.form.get('item_name'))
        app.logger.info(f'item with name: {name} has been added')
        return redirect(url_for('index'))


    @app.route('/remove/<id>', methods=['POST'])
    @login_required
    @roles_accepted('Writer')
    def delete_task(id):
        id = request.form['remove_id']
        mongodbtasks.delete_task(id=request.form['remove_id'])
        app.logger.info(f'item with id: {id} has been removed')
        return redirect(url_for('index'))


    @app.route('/mark_complete/<id>', methods=['POST'])
    @login_required
    @roles_accepted('Writer')
    def mark_complete(id):
        id = request.form['complete_id']
        mongodbtasks.mark_as_completed(id=request.form['complete_id'])
        app.logger.info(f'item with id: {id} has been marked as completed')
        return redirect(url_for('index'))


    @app.route('/mark_doing/<id>', methods=['POST'])
    @login_required 
    @roles_accepted('Writer')
    def mark_doing(id):
        id = request.form['doing_id']
        mongodbtasks.mark_as_doing(id=request.form['doing_id'])
        app.logger.info(f'item with id: {id} has been moved to "doing')
        return redirect(url_for('index'))


    @app.route('/mark_to_do/<id>', methods=['POST'])
    @login_required
    @roles_accepted('Writer')
    def mark_incomplete(id):
        id = request.form['incomplete_id']
        mongodbtasks.mark_as_to_do(id=request.form['incomplete_id'])
        app.logger.info(f'item with id: {id} has been moved to "to do')
        return redirect(url_for('index'))
        

    app.config['LOGIN_DISABLED'] = os.getenv('LOGIN_DISABLED') == 'True'
    return app


if __name__ == "__main__":
    create_app.run(debug=True)


