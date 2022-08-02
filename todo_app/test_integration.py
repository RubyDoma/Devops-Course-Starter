import os
import pytest
import pymongo
import mongomock
from todo_app import app
#from todo_app.mongodb_items import Item
from unittest.mock import Mock
from dotenv import load_dotenv, find_dotenv



file_path = find_dotenv(".env.test")
load_dotenv(file_path, override=True)

connection_string_test = os.environ.get('CONNECTION_STRING_TEST')
client = pymongo.MongoClient(connection_string_test) 


@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    with mongomock.patch(servers=(('fakemongo.com', 27017),)):
        test_app = app.create_app()
        with test_app.test_client() as client:
            yield client
    
def test_index_page(client):
    response = client.get('/')

    assert response.status_code == 200
    assert b'_id' in response.data

class StubResponse():
    def __init__(self, fake_response_data):
        self.fake_response_data = fake_response_data
    def json(self):
        return self.fake_response_data

def get_lists_stub(url):
    client = pymongo.MongoClient(connection_string_test) 
    fake_response_data = []
    if url.startswith(client):
        fake_response_data = [{
        '_id': [{'_id' : "ObjectId('7878556'), 'title' : 'Test item"}]
        }]
        return StubResponse(fake_response_data)
    raise Exception
