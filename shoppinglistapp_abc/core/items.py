"""This module contains the Item and ItemPool classes."""
import math
import random

from shoppinglistapp.core.errors import InvalidItemPriceError, InvalidItemNameError,\
                        InvalidItemPoolError, DuplicateItemError,\
                        NonExistingItemError


class Item:
    """This class represents an item in the store."""
    def __init__(self, name, price):
        if name is None:
            raise InvalidItemNameError(name)
        if not isinstance(name, str):
            raise InvalidItemNameError(name)
        self.name = name
        if not isinstance(price, (float, int)) or not price > 0:
            raise InvalidItemPriceError(price)
        self.price = round(price, 2)

    def get_order(self):
        """Return the order of magnitude of the price of the item."""
        return math.floor(round(math.log(self.price, 10), 10))

    def get_price_str(self, quantity=None, hide_price=False, order=None):
        """Return the price of the item as a string."""
        # price
        if order is None:
            order = self.get_order()
        prc_str = '${:0' + str(order + 4) + '.2f}'
        prc_str = prc_str.format(self.price * (quantity or 1))
        if hide_price:
            prc_str = f'${"?" * (order + 1)}.??'
        return f'{prc_str}'

    def get_list_item_str(self, quantity=None, leading_dash=True):
        """Return the item as a string for a shopping list."""
        # quantity
        if quantity is None:
            qnt_str = ''
        else:
            qnt_str = f' ({quantity}x)'
        # dash
        dash = ''
        if leading_dash:
            dash = '- '
        return f'{dash}{self.name}{qnt_str}'

    def __repr__(self):
        """Return the string representation of the item."""
        return f'Item({self.name}, {self.price})'

    def __eq__(self, other):
        """Return True if the item is equal to the other item,
        False otherwise."""
        return isinstance(other, Item) and self.name == other.name\
            and self.price == other.price


class ItemPool:
    """This class represents a pool of items."""
    def __init__(self, items=None):
        if not items:
            items = {}
        if not isinstance(items, dict):
            raise InvalidItemPoolError()
        for key, val in items.items():
            if not isinstance(key, str) or not isinstance(val, Item):
                raise InvalidItemPoolError()
        self.items = items

    def add_item(self, item):
        """Add an item to the pool."""
        if not isinstance(item, Item):
            raise InvalidItemPoolError()
        if item.name == '':
            raise InvalidItemNameError(item.name)
        if item.name in self.items:
            raise DuplicateItemError()
        self.items[item.name] = item

    def remove_item(self, item_name):
        """Remove an item from the pool."""
        if item_name == '':
            raise InvalidItemNameError(item_name)
        if item_name.isalpha() is False:
            raise InvalidItemNameError(item_name)
        if item_name not in self.items:
            raise NonExistingItemError(item_name)
        del self.items[item_name]

    def get_size(self):
        """Return the size of the pool."""
        return len(self.items)

    def sample_items(self, sample_size):
        """Return a sample of items from the pool."""
        return random.sample(list(self.items.values()),
                             min(sample_size, len(self.items)))

    def __repr__(self):
        """Return the string representation of the pool."""
        return f'ItemPool({self.items})'

    def __eq__(self, other):
        """Return True if the pool is equal to the other pool,
        False otherwise."""
        return isinstance(other, ItemPool) and self.items == other.items
