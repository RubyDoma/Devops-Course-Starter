from flask import Flask, request, render_template, redirect, url_for
from todo_app.data.session_items import get_item, get_items, add_item, remove_item, save_item


from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/', methods=['POST', 'GET'])
def index():
    get_items()
    # sort by status
    return render_template('index.html', get_items=get_items, title='title')


@app.route('/add/add_item', methods=['POST', 'GET'])
def add_to_do():
    if request.method == 'POST':
        add_item(title=request.form.get('item_name'))
        return redirect(url_for('index'))

@app.route('/remove/<item_id>', methods=['POST', 'GET'])
def remove_to_do(item_id):
    get_item(id=int(item_id))
    # items = get_items()
    # for i in items:
    if request.method == 'POST' and request.form['remove'] == 'item':
        remove_item(item=item_id)
    return redirect(url_for('index'))
            

@app.route('/mark_complete', methods=['POST', 'GET'])
def mark_as_complete():
    items = get_items()
    for i in items:
        if request.method == 'POST': 
            i["status"] = "Completed"
            save_item(item=i)
            return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
