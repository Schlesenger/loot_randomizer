import tkinter as tk
from tkinter import ttk
from random import randint, choice
from data import *

class BasePage(ttk.Frame):
    def __init__(self, parent, controller, data):
        super().__init__(parent)
        self.columnconfigure(3, weight = 1)
        self.rowconfigure(3, weight = 1)

        #page navigation
        cr_button = ttk.Button(self, text = 'Treasure by CR', command = lambda: controller.show_frame(EncounterPage))
        cr_button.grid(row = 0, column = 0, sticky = 'nsew')
        item_button = ttk.Button(self, text = 'Random Items by Class', command = lambda: controller.show_frame(ItemPage))
        item_button.grid(row = 0, column = 1, sticky = 'nsew')
        dragon_button = ttk.Button(self, text = 'Dragon Hoard', command = lambda: controller.show_frame(DragonPage))
        dragon_button.grid(row = 0, column = 2, sticky = 'nsew')

        #output & clear buttons
        roll_button = ttk.Button(self, text = 'Roll Loot', command = lambda: self.get_output(self.cr_dropdown))
        roll_button.grid(row = 2, column = 0)
        self.clear_button = ttk.Button(self, text = 'Clear', command = lambda: controller.output_box.delete(0, tk.END))
        self.clear_button.grid(row = 2, column = 1)

        self.data = data

    def get_value_for_range(self, value, dict):
        for key in dict:
            if key[0] <= value <= key[1]:
                return key

class EncounterPage(BasePage):
    def __init__(self, parent, controller, data):
        super().__init__(parent, controller, data)
        self.output_box = controller.output_box

        #dropdown menu for CR ranges
        cr_label = ttk.Label(self, text = 'Chalenge Rating')
        cr_label.grid(row = 1, column = 0)
        cr_choices = ['CR 0-4', 'CR 5-10', 'CR 11-16', 'CR 17+']
        self.cr_dropdown = ttk.Combobox(self, values = cr_choices)
        self.cr_dropdown.current(0)
        self.cr_dropdown.grid(row = 1, column = 2)

    def get_output(self, dropdown):
        value = dropdown.get()
        match value:
            case 'CR 0-4':
                cp, sp, gp = randint(6, 36) * 100, randint(3, 18) * 100, randint(2, 12) * 10
                total_gold = gp + sp % 10 + cp % 100
                print(f'{cp}cp, {sp}sp, {gp}gp, for a total of {total_gold}gp')
                self.output_box.insert(tk.END, f'{cp}cp, {sp}sp, {gp}gp, for a total of {total_gold}gp')

                #random mundane treasures
                percentile = randint (1, 100)
                low = LOOTTABLES['Encounter']['CR 0-4']['Percentile Roll'][self.get_value_for_range(percentile, LOOTTABLES['Encounter']['CR 0-4']['Percentile Roll'])]['low']
                high = LOOTTABLES['Encounter']['CR 0-4']['Percentile Roll'][self.get_value_for_range(percentile, LOOTTABLES['Encounter']['CR 0-4']['Percentile Roll'])]['high']
                object = LOOTTABLES['Encounter']['CR 0-4']['Percentile Roll'][self.get_value_for_range(percentile, LOOTTABLES['Encounter']['CR 0-4']['Percentile Roll'])]['object']
                object_num = randint(low, high)

                #magic item roll 1
                mag_item_1 = randint (1, 100)
                mag_item_2 = randint (1, 100)
                mag_1_low = LOOTTABLES['Encounter']['CR 0-4']['Magic Items'][self.get_value_for_range(mag_item_1, LOOTTABLES['Encounter']['CR 0-4']['Magic Items'])]['low']
                mag_1_high = LOOTTABLES['Encounter']['CR 0-4']['Magic Items'][self.get_value_for_range(mag_item_1, LOOTTABLES['Encounter']['CR 0-4']['Magic Items'])]['high']
                mag_1_object = LOOTTABLES['Encounter']['CR 0-4']['Magic Items'][self.get_value_for_range(mag_item_1, LOOTTABLES['Encounter']['CR 0-4']['Magic Items'])]['object']
                mag_1_num = randint(mag_1_low, mag_1_high)

                #magic item roll 2
                mag_2_low = LOOTTABLES['Encounter']['CR 0-4']['Magic Items'][self.get_value_for_range(mag_item_2, LOOTTABLES['Encounter']['CR 0-4']['Magic Items'])]['low']
                mag_2_high = LOOTTABLES['Encounter']['CR 0-4']['Magic Items'][self.get_value_for_range(mag_item_2, LOOTTABLES['Encounter']['CR 0-4']['Magic Items'])]['high']
                mag_2_object = LOOTTABLES['Encounter']['CR 0-4']['Magic Items'][self.get_value_for_range(mag_item_2, LOOTTABLES['Encounter']['CR 0-4']['Magic Items'])]['object']
                mag_2_num = randint(mag_2_low, mag_2_high)
                
                if object:
                    match object:
                        case '10 gp gems' | '50 gp gems':
                            self.output_box.insert(tk.END, f'{object_num}x{object}')
                            list_of_gems = []
                            for i in range(object_num):
                                list_of_gems.append(randint(1, 12))
                            set_of_gems = set(list_of_gems)
                            for key in set_of_gems:
                                value = GEMSTONES[object][key]
                                count = list_of_gems.count(key)
                                self.output_box.insert(tk.END, f'   {count}x{value}')
                        case '25 gp art objects':
                            self.output_box.insert(tk.END, f'{object_num}x{object}')
                            list_of_art = []
                            for i in range(object_num):
                                list_of_art.append(randint(1, 10))
                            set_of_art = set(list_of_art)
                            for key in set_of_art:
                                value = ARTPIECES[object][key]
                                count = list_of_art.count(key)
                                self.output_box.insert(tk.END, f'   {count}x{value}')

                for obj, num in ((mag_1_object, mag_1_num), (mag_2_object, mag_2_num)):
                    if obj:
                        self.output_box.insert(tk.END, f'{num}x{obj} Items')
                        for i in range(num):
                            mag_item = choice(list(self.data[obj].keys()))
                            self.output_box.insert(tk.END, f'   {self.data[obj][mag_item]['Name']}')
                            
            case 'CR 5-10':
                pass
            case 'CR 11-16':
                pass
            case 'CR 17+':
                pass

class ItemPage(BasePage):
    def __init__(self, parent, controller, data):
        super().__init__(parent, controller, data)

        class_label = ttk.Label(self, text = 'Class')
        class_label.grid(row = 1, column = 0)
        quantity_label = ttk.Label(self, text = 'Quantity')
        quantity_label.grid(row = 2, column = 0)

class DragonPage(BasePage):
    def __init__(self, parent, controller, data):
        super().__init__(parent, controller, data)

        age_label = ttk.Label(self, text = 'Dragon Age')
        age_label.grid(row = 1, column = 0)