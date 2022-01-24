from unittest import result
from todo_app.trello_items import Item
from todo_app.app import ViewModel
    


def test_to_do_items_only_shows_items_in_the_to_do_list():
    # Test Case Setup
    items = []

    to_do_item = Item("1", "ToDoItemName", "To Do")
    items.append(to_do_item)

    doing_item = Item("2", "DoingItemName", "Doing")
    items.append(doing_item)

    done_item = Item("3", "DoneItemName", "Doing")
    items.append(done_item)
    
    view_model = ViewModel(items)

    # End Test Case Setup

    # Start Testing...
    result: list[Item] = view_model.to_do_items

    # Checking everything worked
    assert len(result) == 1
    item = result[0]
    assert item.status == "To Do"
    assert result == [to_do_item] 


