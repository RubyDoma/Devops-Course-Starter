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
    def from_trello_card(cls, card, list_name):
        return cls(card['id'], card['name'], list_name)

        
        
            
    
def fetch_list():

    url = f"https://api.trello.com/1/boards/{board}/lists?key={key}&token={token}&cards=open"
    headers = {
    "Accept": "application/json"
    }

    response = requests.get(url, headers)

    result = response.json()
    

    tasks = []

    for list in result:
        for card in list['cards']:
            task = Item.from_trello_card(card, list["name"])
            tasks.append(task)
    return tasks



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


    return requests.request("DELETE", url=call, headers=headers)



def complete_task_trello(id):

    call = f"https://api.trello.com/1/cards/{id}?idList={done_id}&key={key}&token={token}"

    headers = {
    "Accept": "application/json"
    }



    return requests.request("PUT", url=call, headers=headers)


   

def incomplete_task_trello(id):

    call = f"https://api.trello.com/1/cards/{id}?idList={to_do_id}&key={key}&token={token}"

    headers = {
    "Accept": "application/json"
    }



    return requests.request("PUT", url=call, headers=headers)

    
def doing_task_trello(id):

    call = f"https://api.trello.com/1/cards/{id}?idList={doing_id}&key={key}&token={token}"

    headers = {
    "Accept": "application/json"
    }


    return requests.request("PUT", url=call, headers=headers)

