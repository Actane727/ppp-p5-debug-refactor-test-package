"""Testing module for the shoppinglist_app.py module."""
import pytest
from core.items import Item, ItemPool
from core.shoppinglist import ShoppingList
from core.appengine import AppEngine
from core.errors import InvalidShoppingListSizeError,\
                        InvalidItemPriceError,\
                        InvalidItemNameError,\
                        InvalidItemPoolError,\
                        DuplicateItemError,\
                        NonExistingItemError


def test_app_engine_init():
    """Test the AppEngine class initialization."""
    app_engine = AppEngine()
    assert app_engine.shopping_list is None
    assert app_engine.items is None
    assert app_engine.message is None
    assert app_engine.continue_execution is True
    assert app_engine.correct_answer is None


def test_app_engine_process_answer():
    """Test the AppEngine class process_answer method."""
    app_engine = AppEngine()
    app_engine.correct_answer = 1.00
    app_engine.process_answer('1.00')
    assert app_engine.message == 'Correct!'
    app_engine.correct_answer = 1.00
    app_engine.process_answer('abc')
    app_engine.correct_answer = 1.00
    app_engine.process_answer('2.00')
    assert app_engine.message == ('Not Correct!(Expected $1.00)\n'
                                  'You answered $2.00.')


def test_app_engine_process_add_item():
    """Test the AppEngine class process_add_item method."""
    app_engine = AppEngine()
    app_engine.items = ItemPool()
    app_engine.process_add_item('add orange: abc')
    app_engine.process_add_item('add orange: 1.00')
    app_engine.process_add_item('add orange: 1.00')
    app_engine.process_add_item('add: 1.00')
    app_engine.process_add_item('add : 1.00')


def test_app_engine_process_del_item():
    """Test the AppEngine class process_del_item method."""
    app_engine = AppEngine()
    app_engine.items = ItemPool()
    app_engine.process_del_item('del orange')
    app_engine.process_add_item('add orange: 1.00')
    app_engine.process_del_item('del orange')


def test_shopping_list_init():
    """Test the ShoppingList class initialization."""
    shopping_list = ShoppingList()
    assert not shopping_list.list
    items = ItemPool({'orange': Item('orange', 1),
                      'apple': Item('apple', 2),
                      'lemon': Item('lemon', 3),
                      'banana': Item('banana', 4),
                      'walnut': Item('walnut', 5),
                      'jam': Item('jam', 6)})
    shopping_list = ShoppingList(None, None, item_pool=items)


def test_shopping_list_refresh():
    """Test the ShoppingList class refresh method."""
    items = ItemPool({'orange': Item('orange', 1),
                      'apple': Item('apple', 2),
                      'lemon': Item('lemon', 3),
                      'banana': Item('banana', 4),
                      'walnut': Item('walnut', 5),
                      'jam': Item('jam', 6)})
    shopping_list = ShoppingList(None, None, item_pool=items)
    shopping_list.refresh(items)
    shopping_list = ShoppingList(None, None, item_pool=items)
    shopping_list.refresh(items)
    with pytest.raises(ValueError):
        shopping_list.refresh(items, 4, [1, -1])
    with pytest.raises(ValueError):
        shopping_list.refresh(items, -1, [1, -1])
    with pytest.raises(ValueError):
        shopping_list = ShoppingList('small', None, item_pool=items)
    with pytest.raises(ValueError):
        shopping_list.refresh(items, 'one', {1, 2})
    with pytest.raises(ValueError):
        shopping_list.refresh(items, 4, {1, 2})
    with pytest.raises(ValueError):
        shopping_list.refresh(items, 4, [1, 'one'])
    shopping_list.refresh(items, 4, [1, 2])
    shopping_list.refresh(items, 4, [1, 2, 2, 1, 5, 6, 3, 4])
    with pytest.raises(InvalidShoppingListSizeError):
        shopping_list.refresh(items, 10, [1, 2, 2, 1])


def test_shopping_list_error_check():
    """Test the ShoppingList class error_check method."""
    items = ItemPool({'orange': Item('orange', 1),
                      'apple': Item('apple', 2),
                      'lemon': Item('lemon', 3),
                      'banana': Item('banana', 4),
                      'walnut': Item('walnut', 5),
                      'jam': Item('jam', 6)})
    shopping_list = ShoppingList(None, None, item_pool=items)
    shopping_list.refresh(items, 4, [1, 2, 2, 1])
    with pytest.raises(ValueError):
        shopping_list.error_check(0, None, items)
    with pytest.raises(ValueError):
        shopping_list.error_check(4, {1, 2}, items)
    with pytest.raises(ValueError):
        shopping_list.error_check(4, [1, 'one'], items)
    with pytest.raises(ValueError):
        shopping_list.error_check(4, [1, -1], items)
    with pytest.raises(InvalidShoppingListSizeError):
        shopping_list.error_check(10, [1, 2, 2, 1], items)
    shopping_list.error_check(4, [1, 2, 2], items)
    shopping_list.error_check(4, [1, 2, 2, 1, 5, 6, 3, 4], items)


def test_shopping_list_get_total_price():
    """Test the ShoppingList class get_total_price method."""
    items = ItemPool({'orange': Item('orange', 1.00)})
    shopping_list = ShoppingList(None, None, item_pool=items)
    shopping_list.refresh(items, 1, [1])
    assert shopping_list.get_total_price() == 1.00


def test_shopping_list_get_item_price():
    """Test the ShoppingList class get_item_price method."""
    items = ItemPool({'orange': Item('orange', 1)})
    shopping_list = ShoppingList(None, None, item_pool=items)
    shopping_list.refresh(items, 1, [1])
    assert shopping_list.get_item_price(0) == 1.00


def test_shopping_list_len():
    """Test the ShoppingList class len method."""
    items = ItemPool({'orange': Item('orange', 1),
                      'apple': Item('apple', 2),
                      'lemon': Item('lemon', 3),
                      'banana': Item('banana', 4),
                      'walnut': Item('walnut', 5),
                      'jam': Item('jam', 6)})
    shopping_list = ShoppingList(None, None, item_pool=items)
    shopping_list.refresh(items, 4, [1, 2, 2, 1])
    assert len(shopping_list) == 4


def test_item_init():
    """Test the Item class initialization."""
    item = Item('orange', 1.00)
    assert item.name == 'orange'
    assert item.price == 1.00
    with pytest.raises(InvalidItemNameError):
        item = Item(123, 1.00)
    with pytest.raises(InvalidItemNameError):
        item = Item(None, 0.99)


def test_item_get_order():
    """Test the Item class get_order method."""
    item = Item('orange', 1.00)
    assert item.get_order() == 0


def test_item_get_price_str():
    """Test the Item class get_price_str method."""
    item = Item('orange', 1.00)
    assert item.get_price_str() == '$1.00'
    item = Item('orange', 1.00)
    assert item.get_price_str(hide_price=True) == '$?.??'


def test_item_get_list_item_str():
    """Test the Item class get_list_item_str method."""
    item = Item('orange', 1.00)
    assert item.get_list_item_str() == '- orange'
    item = Item('orange', 1.00)
    assert item.get_list_item_str(
        quantity=2, leading_dash=False) == 'orange (2x)'


def test_item_eq():
    """Test the Item class __eq__ method."""
    item1 = Item('orange', 1.00)
    item2 = Item('orange', 1.00)
    assert item1 == item2
    item1 = Item('orange', 1.00)
    item2 = Item('apple', 1.00)
    assert item1 != item2
    item1 = Item('orange', 1.00)
    item2 = Item('orange', 2.00)
    assert item1 != item2
    item1 = Item('orange', 1.00)
    item2 = Item('apple', 2.00)
    assert item1 != item2


def test_item_pool_init():
    """Test the ItemPool class initialization."""
    item_pool = ItemPool()
    assert item_pool.items == {}
    items = {'orange': Item('orange', 1),
             'apple': Item('apple', 2),
             'lemon': Item('lemon', 3),
             'banana': Item('banana', 4),
             'walnut': Item('walnut', 5),
             'jam': Item('jam', 6)}
    item_pool = ItemPool(items)
    assert item_pool.items == items
    with pytest.raises(InvalidItemPoolError):
        item_pool = ItemPool(123)
    with pytest.raises(InvalidItemPoolError):
        item_pool = ItemPool({'orange': 123})
    with pytest.raises(InvalidItemNameError):
        item_pool = ItemPool({'orange': Item(None, 'abc')})


def test_item_pool_add_item():
    """Test the ItemPool class add_item method."""
    item_pool = ItemPool()
    item = Item('orange', 1.00)
    item_pool.add_item(item)
    assert item_pool.items['orange'].name == 'orange'
    assert item_pool.items['orange'].price == 1.00
    with pytest.raises(InvalidItemNameError):
        item = Item(123, 1.00)
    with pytest.raises(InvalidItemNameError):
        item_pool.add_item(Item('', 1.00))
    with pytest.raises(InvalidItemNameError):
        item = Item(None, 1.00)
    with pytest.raises(InvalidItemPriceError):
        item = Item('orange', 'abc')
    item = Item('orange', 1.00)
    with pytest.raises(DuplicateItemError):
        item_pool.add_item(item)
    with pytest.raises(InvalidItemPoolError):
        item_pool.add_item(None)


def test_item_pool_remove_item():
    """Test the ItemPool class remove_item method."""
    items = {'orange': Item('orange', 1),
             'apple': Item('apple', 2),
             'lemon': Item('lemon', 3),
             'banana': Item('banana', 4),
             'walnut': Item('walnut', 5),
             'jam': Item('jam', 6)}
    item_pool = ItemPool(items)
    item_pool.remove_item('orange')
    assert 'orange' not in item_pool.items
    with pytest.raises(NonExistingItemError):
        item_pool.remove_item('orange')
    with pytest.raises(InvalidItemNameError):
        item_pool.remove_item('')
    with pytest.raises(InvalidItemNameError):
        item_pool.remove_item('123')


def test_item_pool_repr():
    """Test the ItemPool class __repr__ method."""
    item_pool = ItemPool()
    assert repr(item_pool) == 'ItemPool({})'
    items = {'orange': Item('orange', 1.00)}
    item_pool = ItemPool(items)
    assert repr(item_pool) == "ItemPool({'orange': Item(orange, 1.0)})"


def test_item_pool_eq():
    """Test the ItemPool class __eq__ method."""
    item_pool1 = ItemPool()
    item_pool2 = ItemPool()
    assert item_pool1 == item_pool2
    items = {'orange': Item('orange', 1),
             'apple': Item('apple', 2),
             'lemon': Item('lemon', 3),
             'banana': Item('banana', 4),
             'walnut': Item('walnut', 5),
             'jam': Item('jam', 6)}
    item_pool1 = ItemPool(items)
    item_pool2 = ItemPool(items)
    assert item_pool1 == item_pool2
    items = {'orange': Item('orange', 1),
             'apple': Item('apple', 2),
             'lemon': Item('lemon', 3),
             'banana': Item('banana', 4),
             'walnut': Item('walnut', 5),
             'jam': Item('jam', 6)}
    item_pool1 = ItemPool(items)
    item_pool2 = ItemPool()
    assert item_pool1 != item_pool2
    items = {'orange': Item('orange', 1),
             'apple': Item('apple', 2),
             'lemon': Item('lemon', 3),
             'banana': Item('banana', 4),
             'walnut': Item('walnut', 5),
             'jam': Item('jam', 6)}
    item_pool1 = ItemPool(items)
    items = {'orange': Item('orange', 1),
             'apple': Item('apple', 2),
             'lemon': Item('lemon', 3),
             'banana': Item('banana', 4),
             'walnut': Item('walnut', 5),
             'jam': Item('jam', 7)}
    item_pool2 = ItemPool(items)
    assert item_pool1 != item_pool2
    items = {'orange': Item('orange', 1),
             'apple': Item('apple', 2),
             'lemon': Item('lemon', 3),
             'banana': Item('banana', 4),
             'walnut': Item('walnut', 5),
             'jam': Item('jam', 6)}
