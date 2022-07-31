from bson.objectid import ObjectId
import pymongo
import os
from dotenv import find_dotenv, load_dotenv

file_path = find_dotenv(".env")
load_dotenv(file_path, override=True)

connection_string = os.environ.get('CONNECTION_STRING')
client = pymongo.MongoClient(connection_string) 
db_name = os.environ.get('COSMOSODB_NAME')
collection = os.environ.get('COLLECTION_NAME')
tasks = client[f"{db_name}"][f"{collection}"]


class Task:
    def __init__(self, id, title, status):
        self.id = id
        self.title = title
        self.status = status


class MongoDBTasks:
    
    def get_all_tasks(self):
        tasks_list = []
        for task in tasks.find():
            tasks_list.append(Task(id=task["_id"], title=task["title"], status=tasks["status"]))
        return tasks_list
    
    def get_task(self, id):
        id_filter = {"_id": ObjectId(id)}
        task = tasks.find_one(id_filter)

        return task

    def add_task(self, title):
        task = {
            "title": title,
            "status": "To do"
        }
        tasks.insert_one(task)

    def delete_task(self, id):
        id_filter = {"_id": ObjectId(id)}
        tasks.delete_one(id_filter)

   
    def mark_as_completed(self, id):
        id_filter = {"_id": ObjectId(id)}
        update_task_values = {
            "$set": {
                "status": "Done"
            }
        }
        tasks.update_one(id_filter, update_task_values)
    
    def mark_as_doing(self, id):
        id_filter = {"_id": ObjectId(id)}
        update_task_values = {
            "$set": {
                "status": "Doing"
            }
        }
        tasks.update_one(id_filter, update_task_values)
    
    def mark_as_to_do(self, id):
        id_filter = {"_id": ObjectId(id)}
        update_task_values = {
            "$set": {
                "status": "To do"
            }
        }
        tasks.update_one(id_filter, update_task_values)


