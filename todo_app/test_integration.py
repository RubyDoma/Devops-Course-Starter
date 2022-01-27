import os
import requests
from todo_app import app
from unittest.mock import patch, Mock
from dotenv import load_dotenv, find_dotenv

import pytest
from dotenv import load_dotenv, find_dotenv
from todo_app.app import create_app

# @pytest.fixture
# def test_evironment_vars():
#     file_path = find_dotenv('env.test')
#     load_dotenv(file_path, override=True)

@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    with create_app().test_client() as client:
        yield client

def test_index_page(monkeypatch, client):
    monkeypatch.setattr(requests, 'get', get_lists_stub)
    response = client.get('/')

    assert response.status_code == 200
    assert -b'fake data' in response.data

class StubResponse():
    def __init__(self, fake_response_data):
        self.fake_response_data = fake_response_data
    def json(self):
        return self.fake_response_data


def get_lists_stub(url, headers):
    test_board_id = os.environ.get('BOARD_ID')
    fake_response_data = Mock(ok=True)
    if url == f'https://api.trello.com/1/boards/{test_board_id}/lists':
        fake_response_data = [{
        'id': '123abc',
        'name': 'To Do',
        'cards': [{'id': '456', 'name': 'Test card'}]
        }]
        #response.json.return_value = fake_response_data
    return StubResponse(fake_response_data)
    

# sample_trello_lists_response = [{
#     'id': 'to-do-id',
#     'cards': [{
#         'idList': 'to-do-id',
#         'name': 'fake data',
#         'status': "To Do"
#     }, {

#     }]
# }]
    

# def get_lists_stub(url, headers):
#     if url == 'https://api.trello.com/1/boards/pLhPvlZc/lists':
#         response = Mock(ok=True)
#         response.json.return_value = sample_trello_lists_response
#         return response

#     return None
