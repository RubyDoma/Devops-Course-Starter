from flask import Flask, request, render_template, redirect, url_for
from todo_app.data.session_items import get_item, get_items, add_item, remove_item, save_item
import math

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/', methods=['POST', 'GET'])
def index():
    get_items()
    return render_template('index.html', get_items=get_items, title='title')


@app.route('/add/add_item', methods=['POST', 'GET'])
def add_to_do():
    if request.method == 'POST':
        add_item(title=request.form.get('item_name'))
        return redirect(url_for('index'))

@app.route('/remove/', methods=['POST', 'GET'])
def remove_to_do():
    if request.method == 'POST':
        remove_item(title=request.form.get('item_name'))
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
