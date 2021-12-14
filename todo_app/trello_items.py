import requests, os

key = os.environ.get('RUBY_KEY')
token = os.environ.get('RUBY_TOKEN')
board = os.environ.get('BOARD_ID')
to_do_id = os.environ.get('TO_DO_ID')
done_id = os.environ.get('DONE_ID')
doing_id = os.environ.get('DOING_ID')


class Item:
    def __init__(self, id, name, status = 'To Do'):
        self.id = id
        self.name = name
        self.status = status

    @classmethod
    def from_trello_card(cls, card, list):
        return cls(card['id'], card['name'], list['name'])

def fetch_all():
    call = f"https://api.trello.com/1/boards/{board}/lists?key={key}&token={token}&cards=open"
    headers = {
    "Accept": "application/json"
    }

    response = requests.request(
    "GET",
    url=call,
    headers=headers
    )

    result = response.json()

    for item in result:
        if item['name'] == 'To Do':
            return item['cards']

def fetch_done():
    call = f"https://api.trello.com/1/boards/{board}/lists?key={key}&token={token}&cards=open"
    headers = {
    "Accept": "application/json"
    }

    response = requests.request(
    "GET",
    url=call,
    headers=headers
    )

    result = response.json()

    for item in result:
        if item['name'] == 'Done':
            return item['cards']

def fetch_doing():
    call = f"https://api.trello.com/1/boards/{board}/lists?key={key}&token={token}&cards=open"
    headers = {
    "Accept": "application/json"
    }

    response = requests.request(
    "GET",
    url=call,
    headers=headers
    )

    result = response.json()

    for item in result:
        if item['name'] == 'Doing':
            return item['cards']


def add_task_trello(title):

    call = f"https://api.trello.com/1/lists/{to_do_id}/cards?name={title}&key={key}&token={token}"

    headers = {
    "Accept": "application/json"
    }

    response = requests.request(
    "POST",
    url=call,
    headers=headers
    )


def delete_task_trello(id):

    call = f"https://api.trello.com/1/cards/{id}?key={key}&token={token}"

    headers = {
    "Accept": "application/json"
    }


    response = requests.request("DELETE", url=call, headers=headers)


def complete_task_trello(id):

    call = f"https://api.trello.com/1/cards/{id}?idList={done_id}&key={key}&token={token}"

    headers = {
    "Accept": "application/json"
    }


    response = requests.request("PUT", url=call, headers=headers)

   

def incomplete_task_trello(id):

    call = f"https://api.trello.com/1/cards/{id}?idList={to_do_id}&key={key}&token={token}"

    headers = {
    "Accept": "application/json"
    }


    response = requests.request("PUT", url=call, headers=headers)

    print(response.status_code)


def doing_task_trello(id):

    call = f"https://api.trello.com/1/cards/{id}?idList={doing_id}&key={key}&token={token}"

    headers = {
    "Accept": "application/json"
    }


    response = requests.request("PUT", url=call, headers=headers)

    print(response.status_code)