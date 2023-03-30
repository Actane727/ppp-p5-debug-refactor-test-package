"""This module contains the AppEngine class."""
from shoppinglistapp.core.items import Item
from shoppinglistapp.core.errors import InvalidItemNameError, InvalidItemPriceError,\
    NonExistingItemError, DuplicateItemError


class AppEngine:
    """This class is the main engine of the application."""
    def __init__(self, shopping_list=None, items=None):
        self.items = items
        self.shopping_list = shopping_list
        self.continue_execution = True
        self.message = None
        self.correct_answer = None
        self.status = None

    def process_answer(self, cmd):
        """Process the answer to the question."""
        try:
            answer = round(float(cmd), 2)
            if answer == self.correct_answer:
                self.message = 'Correct!'
            else:
                self.message = (f'Not Correct!'
                                f'(Expected ${self.correct_answer:.02f})\n'
                                f'You answered ${answer:.02f}.')
        except ValueError:
            self.message = InvalidItemPriceError(cmd)
        self.correct_answer = None

    def process_add_item(self, cmd):
        """Process the add item command."""
        item_str = cmd[4:]
        item_tuple = item_str.split(': ')
        if len(item_tuple) == 2:
            name, price = item_tuple
            self.validate_add_item(name, price)
        else:
            self.message = f'Cannot add "{item_str}".\n'
            self.message += 'Usage: add <item_name>: <item_price>'

    def process_del_item(self, cmd):
        """Process the delete item command."""
        item_name = cmd[4:]
        try:
            self.items.remove_item(item_name)
            self.message = f'{item_name} removed successfully.'
        except NonExistingItemError:
            self.message = NonExistingItemError(item_name)

    def validate_add_item(self, item, price):
        """Validate the add item command."""
        try:
            try:
                price = float(price)
            except ValueError:
                self.message = InvalidItemPriceError(price)
            if item == '':
                raise InvalidItemNameError(item)
            item = Item(item, price)
            self.items.add_item(item)
            self.message = f'{item} added successfully.'
        except InvalidItemNameError:
            self.message = InvalidItemNameError(item)
        except InvalidItemPriceError:
            self.message = InvalidItemPriceError(price)
        except DuplicateItemError:
            self.message = DuplicateItemError()
