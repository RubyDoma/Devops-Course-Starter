from multiprocessing import allow_connection_pickling
from flask import Flask, request, render_template, redirect, url_for, redirect, jsonify
from todo_app.mongodb_items import MongoDBTasks
from flask_login import LoginManager , login_required, UserMixin
from furl import furl
import os
import json
import requests




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

class User: 

    def __init__(self, id):
        self.id = id

def create_app():
    
    app = Flask(__name__)
    mongodbtasks = MongoDBTasks()

    client_id = os.environ.get('CLIENT_ID')
    client_secret= os.environ.get('CLIENT_SECRET')

    login_manager = LoginManager() 
    @login_manager.unauthorized_handler 
    # Add logic to redirect to the Github OAuth flow when unauthenticated 
    def unauthenticated(): 
        
        url = 'https://github.com/login/oauth/authorize'
        params = {
        'client_id': client_id,
        'redirect_uri': 'http://127.0.0.1:5000/login/callback',
        #'scope': 'read:user',
        #'state': 'An unguessable random string',
       
        }
        url = furl(url).set(params)
        return redirect(str(url), 302)
        

    @app.route('/oauth2/<service>/callback')
    def oauth2_callback(service):
        print(service)

        code = request.args.get('code')
        # access token
        access_token_url = 'https://github.com/login/oauth/access_token'
        payload = {
            'client_id': client_id,
            'client_secret': client_secret,
            'code': code,
            'redirect_uri': 'http://127.0.0.1:5000/login/callback',
            #'state': 'An unguessable random string'
        }
        r = requests.post(access_token_url, json=payload, headers={'Accept': 'application/json'})
        access_token = json.loads(r.text).get('access_token')
        print(access_token)
        # access token
        access_user_url = 'https://api.github.com/user'
        r = requests.get(access_user_url, headers={'Authorization': 'token ' + access_token})
        return jsonify({
            'status': 'success',
            'data': json.loads(r.text)
        })

    
        
    @login_manager.user_loader 
    def load_user(user_id): 
        return None 
    login_manager.init_app(app) 


    @app.route('/')
    @login_required
    def index():
        items = mongodbtasks.get_all_tasks()
        item_view_model = ViewModel(items)
        return render_template('index.html',view_model=item_view_model)
        
            
    @app.route('/add/add_item', methods=['POST'])
    @login_required
    def add_to_do():
        mongodbtasks.add_task(title=request.form.get('item_name'))
        return redirect(url_for('index'))
        

    @app.route('/remove/<id>', methods=['POST'])
    @login_required
    def delete_task(id):
        mongodbtasks.delete_task(id=request.form['remove_id'])
        return redirect(url_for('index'))


    @app.route('/mark_complete/<id>', methods=['POST'])
    @login_required
    def mark_complete(id):
        mongodbtasks.mark_as_completed(id=request.form['complete_id'])
        return redirect(url_for('index'))

    @app.route('/mark_doing/<_id>', methods=['POST'])
    @login_required
    def mark_doing(_id):
        mongodbtasks.mark_as_doing(id=request.form['doing_id'])
        return redirect(url_for('index'))


    @app.route('/mark_to_do/<id>', methods=['POST'])
    @login_required
    def mark_incomplete(id):
        mongodbtasks.mark_as_to_do(id=request.form['incomplete_id'])
        return redirect(url_for('index'))

    return app

if __name__ == "__main__":
    create_app.run(debug=True)


