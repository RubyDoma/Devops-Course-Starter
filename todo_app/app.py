from flask import Flask, request, render_template, redirect, url_for
from todo_app.mongodb_items import MongoDBTasks


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



def create_app():
    
    app = Flask(__name__)
    mongodbtasks = MongoDBTasks()


    @app.route('/')
    def index():
        items = mongodbtasks.get_all_tasks()
        item_view_model = ViewModel(items)
        return render_template('index.html',view_model=item_view_model)
        
            
    @app.route('/add/add_item', methods=['POST'])
    def add_to_do():
        mongodbtasks.add_task(title=request.form.get('item_name'))
        return redirect(url_for('index'))
        

    @app.route('/remove/<id>', methods=['POST'])
    def delete_task(id):
        mongodbtasks.delete_task(id=request.form['remove_id'])
        return redirect(url_for('index'))


    @app.route('/mark_complete/<id>', methods=['POST'])
    def mark_complete(id):
        mongodbtasks.mark_as_completed(id=request.form['complete_id'])
        return redirect(url_for('index'))

    @app.route('/mark_doing/<_id>', methods=['POST'])
    def mark_doing(_id):
        mongodbtasks.mark_as_doing(id=request.form['doing_id'])
        return redirect(url_for('index'))


    @app.route('/mark_to_do/<id>', methods=['POST'])
    def mark_incomplete(id):
        mongodbtasks.mark_as_to_do(id=request.form['incomplete_id'])
        return redirect(url_for('index'))

    return app

if __name__ == "__main__":
    create_app.run(debug=True)