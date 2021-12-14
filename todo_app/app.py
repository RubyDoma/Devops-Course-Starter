from flask import Flask, request, render_template, redirect, url_for
# from todo_app.data.session_items import get_items, add_item, remove_item, save_item, get_item
from todo_app.trello_items import add_task_trello, delete_task_trello, complete_task_trello, fetch_done, fetch_doing, doing_task_trello, incomplete_task_trello, fetch_all



from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', fetch_all=fetch_all, fetch_done=fetch_done, fetch_doing=fetch_doing)

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


