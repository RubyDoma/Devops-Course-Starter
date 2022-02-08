from flask import Flask, request, render_template, redirect, url_for
from todo_app.trello_items import add_task_trello, delete_task_trello, complete_task_trello, fetch_list, doing_task_trello, incomplete_task_trello

from todo_app.flask_config import Config



class ViewModel:
        def __init__(self, items):
            self._items = items

        @property
        def to_do_items(self):
            to_do_output = []
            for item in self._items:
                if item.status == "To Do":
                    to_do_output.append(item)
            return to_do_output
        @property
        def doing_items(self):
            doing_output = []
            for item in self._items:
                if item.status == "Doing":
                    doing_output.append(item)
            return doing_output
        @property
        def done_items(self):
            done_output = []
            for item in self._items:
                if item.status == "Done":
                    done_output.append(item)
            return done_output

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config())


    @app.route('/', methods=['GET'])
    def index():
        items = fetch_list()
        item_view_model = ViewModel(items)
        
        return render_template('index.html', view_model=item_view_model)
        
    @app.route('/add/add_item', methods=['POST'])
    def add_to_do():
        add_task_trello(title=request.form.get('item_name'))

        return redirect(url_for('index'))

    @app.route('/remove/<id>', methods=['POST'])
    def delete_task(id):
        delete_task_trello(id=request.form['remove_id'])
        return redirect(url_for('index'))

    @app.route('/mark_complete/<id>', methods=['POST'])
    def mark_complete(id):
        complete_task_trello(id=request.form['complete_id'])
        return redirect(url_for('index'))

    @app.route('/mark_to_do/<id>', methods=['POST'])
    def mark_incomplete(id):
        incomplete_task_trello(id=request.form['incomplete_id'])
        return redirect(url_for('index'))

    @app.route('/mark_doing/<id>', methods=['POST'])
    def mark_doing(id):
        doing_task_trello(id=request.form['doing_id'])
        return redirect(url_for('index'))


    return app
