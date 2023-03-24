import random
from core.items import Item, ItemPool
from core.shoppinglist import ShoppingList
from core.appengine import AppEngine
# from core.errors import (InvalidItemNameError, InvalidItemPoolError, 
#                          InvalidItemPriceError, InvalidShoppingListSizeError, 
#                          DuplicateItemError, NonExistingItemError)

class AppCLI:
    def __init__(self, shoppingList = None, items = None):
        self.app_engine = AppEngine(shoppingList, items)


    def run(self):
        while True:
            prompt = 'What would you like to do? '
            if self.app_engine.correct_answer is not None:
                prompt = 'What amount should replace the questionmarks? $'
            cmd = input(prompt)
            self.execute_command(cmd)
            print(f'{self.app_engine.message}\n')
            self.app_engine.message = None

            if not self.app_engine.continue_execution:
                break


    def execute_command(self,cmd):
        if self.app_engine.correct_answer is not None:
            self.app_engine.process_answer(cmd)
        elif cmd == 'q' or cmd == 'quit':
            self.app_engine.continue_execution = False
            self.app_engine.message = 'Have a nice day!'
        elif cmd == 'a' or cmd == 'ask':
            self.process_ask()
        elif cmd == 'l' or cmd == 'list':
            self.app_engine.shopping_list.refresh(item_pool = self.app_engine.items)
            self.app_engine.message = (f'Shopping list with {len(self.app_engine.shopping_list)}'
                            f' items has been created.')
        elif cmd.startswith('show'):
            self.process_show(cmd)
        elif cmd.startswith('add'):
            self.app_engine.process_add_item(cmd)
        elif cmd.startswith('del'):
            self.app_engine.process_del_item(cmd)
        else:
            self.app_engine.message = f'"{cmd}" is not a valid command.'


    def process_ask(self):
        q =random.randint(0, len(self.app_engine.shopping_list.list))
        self.app_engine.message= self.show_list(mask_index = q)
        if q<len(self.app_engine.shopping_list.list):
            self.app_engine.correct_answer = self.app_engine.shopping_list.get_item_price(q)
        else:
           self.app_engine.correct_answer = self.app_engine.shopping_list.get_total_price()


    def process_show(self, cmd):
        what = cmd[ 5: ]
        if what == 'items' :
            self.app_engine.message = self.show_items()
        elif what == 'list' :
            self.app_engine.message = self.show_list()
        else:
            self.app_engine.message= f'Cannot show {what}.\n'
            self.app_engine.message += 'Usage: show list|items'


    def show_items(self):
        max_name, max_order = 0, 0
        for item in self.app_engine.items.items.values():
            max_name = max(max_name, len(item.name))
            max_order = max(max_order, item.get_order())
        out = 'ITEMS\n'
        for item_name in sorted(self.app_engine.items.items.keys()):
            item = self.app_engine.items.items[item_name]
            padding = (max_name - len(item_name) + 3) * '.'
            out += (f'{item.get_list_item_str(quantity=None)} {padding} '
                    f'{item.get_price_str(order=max_order)}\n')
        return out


    def show_list(self, mask_index = None):
        q_len = 5
        d_len = 2
        line_base_len = len('TOTAL') - 4
        max_item = max(len(item.name) for item, _ in self.app_engine.shopping_list.list)
        line_base_len = max(max_item, line_base_len) + (q_len - d_len)
        total = Item('TOTAL', self.app_engine.shopping_list.get_total_price())
        max_order = total.get_order()
        max_name = len(total.name)
        for item, _ in self.app_engine.shopping_list.list:
            max_name = max(max_name, len(item.name))
            max_order = max(max_order, item.get_order())
        out = 'SHOPPING LIST\n'
        i = 0
        for i, (item, quantity) in enumerate(self.app_engine.shopping_list.list):
            hide_price = mask_index == i
            padding = (line_base_len - len(item.name)) * '.'
            out += (f'{item.get_list_item_str(quantity)} {padding} '
                     f'{item.get_price_str(quantity, hide_price, max_order)}\n')
        i += 1
        hide_price = mask_index == i
        padding = (line_base_len + d_len) * '.'
        total_line = (f'TOTAL {padding} '
                    f'{total.get_price_str(quantity, order = max_order)}')
        hline = '-'*len(total_line) + '\n'
        return out+hline+total_line + '\n'

if __name__ == '__main__':
    # usage example
    item2 = Item('Macbook', 1999.99)
    item3 = Item('Milk', 4.25)
    item4 = Item('Hotel Room', 255.00)
    item5 = Item('Beef Steak', 25.18)
    ip = ItemPool()
    ip.add_item(item2)
    ip.add_item(item3)
    ip.add_item(item4)
    ip.add_item(item5)
    sp = ShoppingList(size=3, quantities=[3, 2, 4], item_pool=ip)
    app = AppCLI(sp, ip)
    app.run()
