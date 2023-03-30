"""This module contains the ShoppingList class."""
import random
from shoppinglistapp.core.errors import InvalidShoppingListSizeError


class ShoppingList:
    """This class represents a shopping list."""
    def __init__(self, size=None, quantities=None, item_pool=None):
        self.list = []
        if item_pool is not None:
            size, quantities = self.error_check(size, quantities, item_pool)
            self.refresh(item_pool, size, quantities)

    def refresh(self, item_pool, size=None, quantities=None):
        """Refresh the shopping list."""
        if size is None:
            size = random.randint(1, item_pool.get_size())
        if not isinstance(size, int):
            raise ValueError()
        if isinstance(size, int):
            if size < 1:
                raise ValueError()
        if size > item_pool.get_size():
            raise InvalidShoppingListSizeError()
        if quantities is None:
            quantities = random.choices(range(1, 10), k=size)
        if not isinstance(quantities, list):
            raise ValueError()
        for elem in quantities:
            if not isinstance(elem, int):
                raise ValueError()
            if isinstance(elem, int) and elem < 1:
                raise ValueError()
        if len(quantities) < size:
            quantities = quantities + [1] * (size - len(quantities))
        if len(quantities) > size:
            quantities = quantities[:size]
        if isinstance(size, int):
            items_list = item_pool.sample_items(size)
        self.list = list(zip(items_list, quantities))

    def error_check(self, size, quantities, item_pool):
        """Check if the arguments are valid."""
        if size is None:
            size = random.randint(1, item_pool.get_size())
        if not isinstance(size, int):
            raise ValueError()
        if isinstance(size, int):
            if size < 1:
                raise ValueError()
        if size > item_pool.get_size():
            raise InvalidShoppingListSizeError()
        if quantities is None:
            quantities = random.choices(range(1, 10), k=size)
        if not isinstance(quantities, list):
            raise ValueError()
        for elem in quantities:
            if not isinstance(elem, int):
                raise ValueError()
            if isinstance(elem, int) and elem < 1:
                raise ValueError()
        if len(quantities) < size:
            quantities = quantities + [1] * (size - len(quantities))
        if len(quantities) > size:
            quantities = quantities[:size]
        return size, quantities

    def get_total_price(self):
        """Return the total price of the shopping list."""
        return round(sum(item.price * qnt for (item, qnt) in self.list), 2)

    def get_item_price(self, i):
        """Return the price of the i-th item in the shopping list."""
        return round(self.list[i][0].price * self.list[i][1], 2)

    def __len__(self):
        """Return the length of the shopping list."""
        return len(self.list)
