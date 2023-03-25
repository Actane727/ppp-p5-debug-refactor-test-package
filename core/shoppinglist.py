import random
from core.errors import InvalidShoppingListSizeError

class ShoppingList:
    def __init__(self, size = None, quantities = None, item_pool = None):
        self.list = []
        if item_pool is not None:
            self.refresh(item_pool, size, quantities)

    def refresh(self, item_pool, size = None, quantities = None):
        if size is None:
            size = random.randint(1,item_pool.get_size())
        if type(size) != int or size < 1:
            raise ValueError()
        if size > item_pool.get_size():
            raise InvalidShoppingListSizeError()
        if quantities is None:
            quantities = random.choices(range(1, 10), k=size)
        if type(quantities) != list:
            raise ValueError()
        for elem in quantities:
            if type(elem) != int or elem < 1:
                raise ValueError()
        if len(quantities) < size:
            quantities = quantities + [1] * (size - len(quantities))
        if len(quantities) > size:
            quantities = quantities[:size]
        items_list = item_pool.sample_items(size)
        self.list = [(item, q) for item, q in zip(items_list, quantities)]

    def get_total_price(self):
        return round(sum([item.price * qnt for item, qnt in self.list]), 2)

    def get_item_price(self, i):
        return round(self.list[i][0].price * self.list[i][1], 2)


    def __len__(self):
        return len(self.list)
