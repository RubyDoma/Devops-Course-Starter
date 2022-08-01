import os
import pytest
import pymongo
import mongomock
from todo_app import app
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
    