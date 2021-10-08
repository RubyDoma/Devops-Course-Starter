from flask import Flask, request, render_template, redirect, url_for
from todo_app.data.session_items import get_items, add_item, remove_item, save_item


from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/', methods=['POST', 'GET'])
def index():
    items = get_items()
    #sorted(items, key = lambda item: item['status'], reverse=True)
    return render_template('index.html', get_items=get_items, items=items, title='title')


@app.route('/add/add_item', methods=['POST', 'GET'])
def add_to_do():
    if request.method == 'POST':
        add_item(title=request.form.get('item_name'))
        return redirect(url_for('index'))

@app.route('/remove/<item_id>', methods=['POST'])
def remove_to_do(item_id):
    items = get_items()
    for item in items:
        if item['id'] == int(item_id):
            remove_item(item=item)
    return redirect(url_for('index'))    
            

@app.route('/mark_complete/<item_id>', methods=['POST', 'GET'])
def mark_as_complete(item_id):
    items = get_items()
    for item in items:
        if item['id'] == int(item_id):
            item["status"] = "Completed"
            save_item(item=item)
            sorted(item.keys())
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run()
