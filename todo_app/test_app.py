from unittest import result
from todo_app.trello_items import Item
from todo_app.app import ViewModel
    


def test_to_do_items_only_shows_items_in_the_to_do_list():
    to_do_item = Item("1", "ToDoItemName", "To Do")
    doing_item = Item("2", "DoingItemName", "Doing")
    done_item = Item("3", "DoneItemName", "Doing")
    
    view_model = ViewModel([to_do_item, doing_item, done_item])
    result = view_model.to_do_items

    assert result == [to_do_item]


