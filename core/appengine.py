from core.items import Item
from core.errors import InvalidItemNameError, InvalidItemPriceError, InvalidItemPoolError, NonExistingItemError, DuplicateItemError, InvalidShoppingListSizeError


class AppEngine:
    def __init__(self, shoppingList = None, items = None):
        self.items = items
        self.shopping_list = shoppingList
        self.continue_execution = True
        self.message = None
        self.correct_answer = None
        self.status = None


    def process_answer(self, cmd):
        try:
            answer = round(float(cmd), 2)
            if answer == self.correct_answer:
                self.message = 'Correct!'
            else:
                self.message = (f'Not Correct! (Expected ${self.correct_answer:.02f})\n'
                                f'You answered ${answer:.02f}.')
        except ValueError:
            self.message = InvalidItemPriceError(cmd)
        self.correct_answer = None


    def process_add_item(self, cmd):
        item_str = cmd[4:]
        item_tuple = item_str.split(': ')
        if len(item_tuple)==2:
            name, price = item_tuple
            self.validate_add_item(name, price)
        else:
            self.message = f'Cannot add "{item_str}".\n'
            self.message += 'Usage: add <item_name>: <item_price>'


    def process_del_item(self, cmd):
        item_name = cmd[4: ]
        try:
            self.items.remove_item(item_name)
            self.message =f'{item_name} removed successfully.'
        except NonExistingItemError as e:  
            self.message = e

    def validate_add_item(self, item, price):
        try:
            isinstance(item, str) is True
            try:
                price = float(price)
            except ValueError:
                self.message = InvalidItemPriceError(price)
            item = Item(item, price)
            type(item) is Item is True
            self.items.add_item(item)
            self.message = f'{item} added successfully.'        
        except InvalidItemNameError as e:
            self.message = e
        except InvalidItemPriceError as e:
            self.message = e
        except DuplicateItemError as e:
            self.message = e

