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
    
    def roll_dice(self, dice_num, dice_size):
        total = 0
        for i in range(dice_num):
            total += randint(1,dice_size)
        return total

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
                cp, sp, gp = self.roll_dice(6, 6) * 100, self.roll_dice(3, 6) * 100, self.roll_dice(2, 6) * 10
                total_gold = gp + sp % 10 + cp % 100
                self.output_box.insert(tk.END, f'{cp}cp, {sp}sp, {gp}gp, for a total of {total_gold}gp')

                #random mundane treasures
                percentile = randint (1, 100)
                dice_num = LOOTTABLES['Encounter']['CR 0-4']['Percentile Roll'][self.get_value_for_range(percentile, LOOTTABLES['Encounter']['CR 0-4']['Percentile Roll'])]['dice_num']
                dice_size = LOOTTABLES['Encounter']['CR 0-4']['Percentile Roll'][self.get_value_for_range(percentile, LOOTTABLES['Encounter']['CR 0-4']['Percentile Roll'])]['dice_size']
                object = LOOTTABLES['Encounter']['CR 0-4']['Percentile Roll'][self.get_value_for_range(percentile, LOOTTABLES['Encounter']['CR 0-4']['Percentile Roll'])]['object']
                object_num = self.roll_dice(dice_num, dice_size)

                #magic item roll 1
                mag_1_dice_num = LOOTTABLES['Encounter']['CR 0-4']['Magic Items'][self.get_value_for_range(percentile, LOOTTABLES['Encounter']['CR 0-4']['Magic Items'])]['dice_num']
                mag_1_dice_size = LOOTTABLES['Encounter']['CR 0-4']['Magic Items'][self.get_value_for_range(percentile, LOOTTABLES['Encounter']['CR 0-4']['Magic Items'])]['dice_size']
                mag_1_object = LOOTTABLES['Encounter']['CR 0-4']['Magic Items'][self.get_value_for_range(percentile, LOOTTABLES['Encounter']['CR 0-4']['Magic Items'])]['object']
                mag_1_num = self.roll_dice(mag_1_dice_num, mag_1_dice_size)

                #magic item roll 2
                mag_item_roll = randint (1, 100)
                mag_2_dice_num = LOOTTABLES['Encounter']['CR 0-4']['Magic Items'][self.get_value_for_range(mag_item_roll, LOOTTABLES['Encounter']['CR 0-4']['Magic Items'])]['dice_num']
                mag_2_dice_size = LOOTTABLES['Encounter']['CR 0-4']['Magic Items'][self.get_value_for_range(mag_item_roll, LOOTTABLES['Encounter']['CR 0-4']['Magic Items'])]['dice_size']
                mag_2_object = LOOTTABLES['Encounter']['CR 0-4']['Magic Items'][self.get_value_for_range(mag_item_roll, LOOTTABLES['Encounter']['CR 0-4']['Magic Items'])]['object']
                mag_2_num = self.roll_dice(mag_2_dice_num, mag_2_dice_size)
                
                if object:
                    match object:
                        case '10 gp gems':
                            self.output_box.insert(tk.END, f'{object_num}x{object}')
                            list_of_gems = []
                            for i in range(object_num):
                                list_of_gems.append(randint(1, 12))
                            set_of_gems = set(list_of_gems)
                            for key in set_of_gems:
                                value = GEMSTONES[object][key]
                                count = list_of_gems.count(key)
                                self.output_box.insert(tk.END, f'   {count}x{value}')
                            self.output_box.insert(tk.END, f' total gp value of {total_gold + (object_num * 10)}gp')
                        case '50 gp gems':
                            self.output_box.insert(tk.END, f'{object_num}x{object}')
                            list_of_gems = []
                            for i in range(object_num):
                                list_of_gems.append(randint(1, 12))
                            set_of_gems = set(list_of_gems)
                            for key in set_of_gems:
                                value = GEMSTONES[object][key]
                                count = list_of_gems.count(key)
                                self.output_box.insert(tk.END, f'   {count}x{value}')
                            self.output_box.insert(tk.END, f' total gp value of {total_gold + (object_num * 50)}gp')
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
                            self.output_box.insert(tk.END, f' total gp value of {total_gold + (object_num * 25)}gp')

                for obj, num in ((mag_1_object, mag_1_num), (mag_2_object, mag_2_num)):
                    if obj:
                        self.output_box.insert(tk.END, f'{num}x{obj} Items')
                        for i in range(num):
                            mag_item = choice(list(self.data[obj].keys()))
                            self.output_box.insert(tk.END, f'   {self.data[obj][mag_item]['Name']}')
                            
            case 'CR 5-10':
                cp, sp, gp, pp = self.roll_dice(2, 6) * 100, self.roll_dice(2, 6) * 1000, self.roll_dice(6, 6) * 100, self.roll_dice(3, 6) * 10
                total_gold = pp * 10 + gp + sp % 10 + cp % 100
                self.output_box.insert(tk.END, f'{cp}cp, {sp}sp, {gp}gp, {pp}pp, for a total of {total_gold}gp')

                #random mundane treasures
                percentile = randint (1, 100)
                dice_num = LOOTTABLES['Encounter']['CR 5-10']['Percentile Roll'][self.get_value_for_range(percentile, LOOTTABLES['Encounter']['CR 5-10']['Percentile Roll'])]['dice_num']
                dice_size = LOOTTABLES['Encounter']['CR 5-10']['Percentile Roll'][self.get_value_for_range(percentile, LOOTTABLES['Encounter']['CR 5-10']['Percentile Roll'])]['dice_size']
                object = LOOTTABLES['Encounter']['CR 5-10']['Percentile Roll'][self.get_value_for_range(percentile, LOOTTABLES['Encounter']['CR 5-10']['Percentile Roll'])]['object']
                object_num = self.roll_dice(dice_num, dice_size)

                #magic item roll 1
                mag_1_dice_num = LOOTTABLES['Encounter']['CR 5-10']['Magic Items'][self.get_value_for_range(percentile, LOOTTABLES['Encounter']['CR 5-10']['Magic Items'])]['dice_num']
                mag_1_dice_size = LOOTTABLES['Encounter']['CR 5-10']['Magic Items'][self.get_value_for_range(percentile, LOOTTABLES['Encounter']['CR 5-10']['Magic Items'])]['dice_size']
                mag_1_object = LOOTTABLES['Encounter']['CR 5-10']['Magic Items'][self.get_value_for_range(percentile, LOOTTABLES['Encounter']['CR 5-10']['Magic Items'])]['object']
                mag_1_num = self.roll_dice(mag_1_dice_num, mag_1_dice_size)

                #magic item roll 2
                mag_item_roll = randint (1, 100)
                mag_2_dice_num = LOOTTABLES['Encounter']['CR 5-10']['Magic Items'][self.get_value_for_range(mag_item_roll, LOOTTABLES['Encounter']['CR 5-10']['Magic Items'])]['dice_num']
                mag_2_dice_size = LOOTTABLES['Encounter']['CR 5-10']['Magic Items'][self.get_value_for_range(mag_item_roll, LOOTTABLES['Encounter']['CR 5-10']['Magic Items'])]['dice_size']
                mag_2_object = LOOTTABLES['Encounter']['CR 5-10']['Magic Items'][self.get_value_for_range(mag_item_roll, LOOTTABLES['Encounter']['CR 5-10']['Magic Items'])]['object']
                mag_2_num = self.roll_dice(mag_2_dice_num, mag_2_dice_size)
                
                if object:
                    match object:
                        case '50 gp gems':
                            self.output_box.insert(tk.END, f'{object_num}x{object}')
                            list_of_gems = []
                            for i in range(object_num):
                                list_of_gems.append(randint(1, 12))
                            set_of_gems = set(list_of_gems)
                            for key in set_of_gems:
                                value = GEMSTONES[object][key]
                                count = list_of_gems.count(key)
                                self.output_box.insert(tk.END, f'   {count}x{value}')
                            self.output_box.insert(tk.END, f' total gp value of {total_gold + (object_num * 50)}gp')
                        case '100 gp gems':
                            self.output_box.insert(tk.END, f'{object_num}x{object}')
                            list_of_gems = []
                            for i in range(object_num):
                                list_of_gems.append(randint(1, 10))
                            set_of_gems = set(list_of_gems)
                            for key in set_of_gems:
                                value = GEMSTONES[object][key]
                                count = list_of_gems.count(key)
                                self.output_box.insert(tk.END, f'   {count}x{value}')
                            self.output_box.insert(tk.END, f' total gp value of {total_gold + (object_num * 100)}gp')
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
                            self.output_box.insert(tk.END, f' total gp value of {total_gold + (object_num * 25)}gp')
                        case '250 gp art objects':
                            self.output_box.insert(tk.END, f'{object_num}x{object}')
                            list_of_gems = []
                            for i in range(object_num):
                                list_of_gems.append(randint(1, 10))
                            set_of_gems = set(list_of_gems)
                            for key in set_of_gems:
                                value = GEMSTONES[object][key]
                                count = list_of_gems.count(key)
                                self.output_box.insert(tk.END, f'   {count}x{value}')
                            self.output_box.insert(tk.END, f' total gp value of {total_gold + (object_num * 250)}gp')

                for obj, num in ((mag_1_object, mag_1_num), (mag_2_object, mag_2_num)):
                    if obj:
                        self.output_box.insert(tk.END, f'{num}x{obj} Items')
                        for i in range(num):
                            mag_item = choice(list(self.data[obj].keys()))
                            self.output_box.insert(tk.END, f'   {self.data[obj][mag_item]['Name']}')

            case 'CR 11-16':
                gp, pp = self.roll_dice(4, 6) * 1000, self.roll_dice(5, 6) * 100
                total_gold = pp * 10 + gp
                self.output_box.insert(tk.END, f'{gp}gp, {pp}pp, for a total of {total_gold}gp')

                #random mundane treasures
                percentile = randint (1, 100)
                dice_num = LOOTTABLES['Encounter']['CR 11-16']['Percentile Roll'][self.get_value_for_range(percentile, LOOTTABLES['Encounter']['CR 11-16']['Percentile Roll'])]['dice_num']
                dice_size = LOOTTABLES['Encounter']['CR 11-16']['Percentile Roll'][self.get_value_for_range(percentile, LOOTTABLES['Encounter']['CR 11-16']['Percentile Roll'])]['dice_size']
                object = LOOTTABLES['Encounter']['CR 11-16']['Percentile Roll'][self.get_value_for_range(percentile, LOOTTABLES['Encounter']['CR 11-16']['Percentile Roll'])]['object']
                object_num = self.roll_dice(dice_num, dice_size)

                #magic item roll 1
                mag_1_dice_num = LOOTTABLES['Encounter']['CR 11-16']['Magic Items'][self.get_value_for_range(percentile, LOOTTABLES['Encounter']['CR 11-16']['Magic Items'])]['dice_num']
                mag_1_dice_size = LOOTTABLES['Encounter']['CR 11-16']['Magic Items'][self.get_value_for_range(percentile, LOOTTABLES['Encounter']['CR 11-16']['Magic Items'])]['dice_size']
                mag_1_object = LOOTTABLES['Encounter']['CR 11-16']['Magic Items'][self.get_value_for_range(percentile, LOOTTABLES['Encounter']['CR 11-16']['Magic Items'])]['object']
                mag_1_num = self.roll_dice(mag_1_dice_num, mag_1_dice_size)

                #magic item roll 2
                mag_item_roll = randint (1, 100)
                mag_2_dice_num = LOOTTABLES['Encounter']['CR 11-16']['Magic Items'][self.get_value_for_range(mag_item_roll, LOOTTABLES['Encounter']['CR 11-16']['Magic Items'])]['dice_num']
                mag_2_dice_size = LOOTTABLES['Encounter']['CR 11-16']['Magic Items'][self.get_value_for_range(mag_item_roll, LOOTTABLES['Encounter']['CR 11-16']['Magic Items'])]['dice_size']
                mag_2_object = LOOTTABLES['Encounter']['CR 11-16']['Magic Items'][self.get_value_for_range(mag_item_roll, LOOTTABLES['Encounter']['CR 11-16']['Magic Items'])]['object']
                mag_2_num = self.roll_dice(mag_2_dice_num, mag_2_dice_size)
                
                if object:
                    match object:
                        case '500 gp gems':
                            self.output_box.insert(tk.END, f'{object_num}x{object}')
                            list_of_gems = []
                            for i in range(object_num):
                                list_of_gems.append(randint(1, 6))
                            set_of_gems = set(list_of_gems)
                            for key in set_of_gems:
                                value = GEMSTONES[object][key]
                                count = list_of_gems.count(key)
                                self.output_box.insert(tk.END, f'   {count}x{value}')
                            self.output_box.insert(tk.END, f' total gp value of {total_gold + (object_num * 500)}gp')
                        case '1000 gp gems':
                            self.output_box.insert(tk.END, f'{object_num}x{object}')
                            list_of_gems = []
                            for i in range(object_num):
                                list_of_gems.append(randint(1, 8))
                            set_of_gems = set(list_of_gems)
                            for key in set_of_gems:
                                value = GEMSTONES[object][key]
                                count = list_of_gems.count(key)
                                self.output_box.insert(tk.END, f'   {count}x{value}')
                            self.output_box.insert(tk.END, f' total gp value of {total_gold + (object_num * 100)}gp')
                        case '250 gp art objects':
                            self.output_box.insert(tk.END, f'{object_num}x{object}')
                            list_of_art = []
                            for i in range(object_num):
                                list_of_art.append(randint(1, 10))
                            set_of_art = set(list_of_art)
                            for key in set_of_art:
                                value = ARTPIECES[object][key]
                                count = list_of_art.count(key)
                                self.output_box.insert(tk.END, f'   {count}x{value}')
                            self.output_box.insert(tk.END, f' total gp value of {total_gold + (object_num * 250)}gp')
                        case '750 gp art objects':
                            self.output_box.insert(tk.END, f'{object_num}x{object}')
                            list_of_gems = []
                            for i in range(object_num):
                                list_of_gems.append(randint(1, 10))
                            set_of_gems = set(list_of_gems)
                            for key in set_of_gems:
                                value = ARTPIECES[object][key]
                                count = list_of_gems.count(key)
                                self.output_box.insert(tk.END, f'   {count}x{value}')
                            self.output_box.insert(tk.END, f' total gp value of {total_gold + (object_num * 750)}gp')

                for obj, num in ((mag_1_object, mag_1_num), (mag_2_object, mag_2_num)):
                    if obj:
                        self.output_box.insert(tk.END, f'{num}x{obj} Items')
                        for i in range(num):
                            mag_item = choice(list(self.data[obj].keys()))
                            self.output_box.insert(tk.END, f'   {self.data[obj][mag_item]['Name']}')

            case 'CR 17+':
                gp, pp = self.roll_dice(12, 6) * 1000, self.roll_dice(8, 6) * 1000
                total_gold = pp * 10 + gp
                self.output_box.insert(tk.END, f'{gp}gp, {pp}pp, for a total of {total_gold}gp')

                #random mundane treasures
                percentile = randint (1, 100)
                dice_num = LOOTTABLES['Encounter']['CR 17+']['Percentile Roll'][self.get_value_for_range(percentile, LOOTTABLES['Encounter']['CR 17+']['Percentile Roll'])]['dice_num']
                dice_size = LOOTTABLES['Encounter']['CR 17+']['Percentile Roll'][self.get_value_for_range(percentile, LOOTTABLES['Encounter']['CR 17+']['Percentile Roll'])]['dice_size']
                object = LOOTTABLES['Encounter']['CR 17+']['Percentile Roll'][self.get_value_for_range(percentile, LOOTTABLES['Encounter']['CR 17+']['Percentile Roll'])]['object']
                object_num = self.roll_dice(dice_num, dice_size)

                #magic item roll 1
                mag_1_dice_num = LOOTTABLES['Encounter']['CR 17+']['Magic Items'][self.get_value_for_range(percentile, LOOTTABLES['Encounter']['CR 17+']['Magic Items'])]['dice_num']
                mag_1_dice_size = LOOTTABLES['Encounter']['CR 17+']['Magic Items'][self.get_value_for_range(percentile, LOOTTABLES['Encounter']['CR 17+']['Magic Items'])]['dice_size']
                mag_1_object = LOOTTABLES['Encounter']['CR 17+']['Magic Items'][self.get_value_for_range(percentile, LOOTTABLES['Encounter']['CR 17+']['Magic Items'])]['object']
                mag_1_num = self.roll_dice(mag_1_dice_num, mag_1_dice_size)

                #magic item roll 2
                mag_item_roll = randint (1, 100)
                mag_2_dice_num = LOOTTABLES['Encounter']['CR 17+']['Magic Items'][self.get_value_for_range(mag_item_roll, LOOTTABLES['Encounter']['CR 17+']['Magic Items'])]['dice_num']
                mag_2_dice_size = LOOTTABLES['Encounter']['CR 17+']['Magic Items'][self.get_value_for_range(mag_item_roll, LOOTTABLES['Encounter']['CR 17+']['Magic Items'])]['dice_size']
                mag_2_object = LOOTTABLES['Encounter']['CR 17+']['Magic Items'][self.get_value_for_range(mag_item_roll, LOOTTABLES['Encounter']['CR 17+']['Magic Items'])]['object']
                mag_2_num = self.roll_dice(mag_2_dice_num, mag_2_dice_size)
                
                if object:
                    match object:
                        case '1000 gp gems':
                            self.output_box.insert(tk.END, f'{object_num}x{object}')
                            list_of_gems = []
                            for i in range(object_num):
                                list_of_gems.append(randint(1, 8))
                            set_of_gems = set(list_of_gems)
                            for key in set_of_gems:
                                value = GEMSTONES[object][key]
                                count = list_of_gems.count(key)
                                self.output_box.insert(tk.END, f'   {count}x{value}')
                            self.output_box.insert(tk.END, f' total gp value of {total_gold + (object_num * 1000)}gp')
                        case '5000 gp gems':
                            self.output_box.insert(tk.END, f'{object_num}x{object}')
                            list_of_gems = []
                            for i in range(object_num):
                                list_of_gems.append(randint(1, 4))
                            set_of_gems = set(list_of_gems)
                            for key in set_of_gems:
                                value = GEMSTONES[object][key]
                                count = list_of_gems.count(key)
                                self.output_box.insert(tk.END, f'   {count}x{value}')
                            self.output_box.insert(tk.END, f' total gp value of {total_gold + (object_num * 5000)}gp')
                        case '2500 gp art objects':
                            self.output_box.insert(tk.END, f'{object_num}x{object}')
                            list_of_art = []
                            for i in range(object_num):
                                list_of_art.append(randint(1, 10))
                            set_of_art = set(list_of_art)
                            for key in set_of_art:
                                value = ARTPIECES[object][key]
                                count = list_of_art.count(key)
                                self.output_box.insert(tk.END, f'   {count}x{value}')
                            self.output_box.insert(tk.END, f' total gp value of {total_gold + (object_num * 2500)}gp')
                        case '7500 gp art objects':
                            self.output_box.insert(tk.END, f'{object_num}x{object}')
                            list_of_gems = []
                            for i in range(object_num):
                                list_of_gems.append(randint(1, 8))
                            set_of_gems = set(list_of_gems)
                            for key in set_of_gems:
                                value = ARTPIECES[object][key]
                                count = list_of_gems.count(key)
                                self.output_box.insert(tk.END, f'   {count}x{value}')
                            self.output_box.insert(tk.END, f' total gp value of {total_gold + (object_num * 7500)}gp')

                for obj, num in ((mag_1_object, mag_1_num), (mag_2_object, mag_2_num)):
                    if obj:
                        self.output_box.insert(tk.END, f'{num}x{obj} Items')
                        for i in range(num):
                            mag_item = choice(list(self.data[obj].keys()))
                            self.output_box.insert(tk.END, f'   {self.data[obj][mag_item]['Name']}')

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