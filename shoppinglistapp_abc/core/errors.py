"""This module contains all the custom exceptions used in the project."""


class InvalidItemNameError(Exception):
    """This exception is raised when an invalid
    item name is passed to the Item"""
    def __init__(self, item):
        if not isinstance(item, str):
            super().__init__(f'Item name must be a string (not {type(item)}).')
        else:
            super().__init__('Item name string cannot be empty.')


class InvalidItemPriceError(Exception):
    """This exception is raised when an invalid item price
    is passed to the Item"""
    def __init__(self, price):
        super().__init__(f'The price argument ("{price}") does not '
                         f'appear to be any of the following: float, '
                         f'an integer, or a string that can be parsed '
                         f'to a non-negative float.')


class InvalidItemPoolError(Exception):
    """This exception is raised when an invalid item pool is
    passed to the ItemPool"""
    def __init__(self):
        super().__init__('ItemsPool needs to be set as a dictionary '
                         'with non-empty strings as keys and Item instances '
                         'as values.')


class NonExistingItemError(Exception):
    """This exception is raised when an item is not present in
    the item pool."""
    def __init__(self, item_name):
        super().__init__(f'Item named "{item_name}" is not present '
                         f'in the item pool.')


class DuplicateItemError(Exception):
    """This exception is raised when an item is already present
    in the item pool."""
    def __init__(self):
        super().__init__('Duplicate!')


class InvalidShoppingListSizeError(Exception):
    """This exception is raised when an invalid shopping list size
    is passed to the"""
    def __init__(self):
        super().__init__('Invalid List Size!')
