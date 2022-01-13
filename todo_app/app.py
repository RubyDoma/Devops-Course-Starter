from flask import Flask, request, render_template, redirect, url_for
from todo_app.trello_items import add_task_trello, delete_task_trello, complete_task_trello, fetch_list, doing_task_trello, incomplete_task_trello


from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())

class ViewModel:
    def __init__(self, to_do_items, doing_items, done_items):
        self._to_do_items = to_do_items
        self._doing_items = doing_items
        self._done_items = done_items
    @property
    def to_do_items(self):
        return self._to_do_items
    @property
    def doing_items(self):
        return self._doing_items
    @property
    def done_items(self):
        return self._done_items

to_do_items = fetch_list("To Do")
doing_items = fetch_list("Doing")
done_items = fetch_list("Done")
item_view_model = ViewModel(to_do_items, doing_items, done_items)

@app.route('/', methods=['GET'])
def index():
    
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

    

if __name__ == '__main__':
    app.run()


