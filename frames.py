import tkinter as tk
from tkinter import ttk
from random import randint, choice
from data import *
from collections import Counter

class BasePage(ttk.Frame):
    def __init__(self, parent, controller, data):
        super().__init__(parent)
        self.output_box = controller.output_box

        #page navigation
        cr_button = ttk.Button(self, text = 'Treasure by CR', command = lambda: controller.show_frame(EncounterPage))
        cr_button.grid(row = 0, column = 0, sticky = 'nsew')
        item_button = ttk.Button(self, text = 'Random Items by Class', command = lambda: controller.show_frame(ItemPage))
        item_button.grid(row = 0, column = 1, sticky = 'nsew')
        parcel_button = ttk.Button(self, text = 'Parcels', command = lambda: controller.show_frame(ParcelPage))
        parcel_button.grid(row = 0, column = 2, sticky = 'nsew')

        #clear button
        self.clear_button = ttk.Button(self, text = 'Clear', command = lambda: controller.output_box.delete(0, tk.END))
        self.clear_button.grid(row = 3, column = 1, sticky = 'nsew')

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

        #dropdown menu for CR ranges
        cr_label = ttk.Label(self, text = 'Chalenge Rating')
        cr_label.grid(row = 1, column = 0, sticky = 'w')
        cr_choices = ['CR 0-4', 'CR 5-10', 'CR 11-16', 'CR 17+']
        self.cr_dropdown = ttk.Combobox(self, values = cr_choices)
        self.cr_dropdown.current(0)
        self.cr_dropdown.grid(row = 1, column = 2)

        #output button
        roll_button = ttk.Button(self, text = 'Roll Loot', command = lambda: self.get_output(self.cr_dropdown))
        roll_button.grid(row = 3, column = 0, sticky = 'nsew')

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
                            if self.data[obj][mag_item]['Cursed'] == 'Y':
                                self.output_box.insert(tk.END, f'   {self.data[obj][mag_item]['Name']}(CURSED)')
                            else:
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
                                value = ARTPIECES[object][key]
                                count = list_of_gems.count(key)
                                self.output_box.insert(tk.END, f'   {count}x{value}')
                            self.output_box.insert(tk.END, f' total gp value of {total_gold + (object_num * 250)}gp')

                for obj, num in ((mag_1_object, mag_1_num), (mag_2_object, mag_2_num)):
                    if obj:
                        self.output_box.insert(tk.END, f'{num}x{obj} Items')
                        for i in range(num):
                            mag_item = choice(list(self.data[obj].keys()))
                            if self.data[obj][mag_item]['Cursed'] == 'Y':
                                self.output_box.insert(tk.END, f'   {self.data[obj][mag_item]['Name']}(CURSED)')
                            else:
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
                            if self.data[obj][mag_item]['Cursed'] == 'Y':
                                self.output_box.insert(tk.END, f'   {self.data[obj][mag_item]['Name']}(CURSED)')
                            else:
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
                            if self.data[obj][mag_item]['Cursed'] == 'Y':
                                self.output_box.insert(tk.END, f'   {self.data[obj][mag_item]['Name']}(CURSED)')
                            else:
                                self.output_box.insert(tk.END, f'   {self.data[obj][mag_item]['Name']}')

class ItemPage(BasePage):
    def __init__(self, parent, controller, data):
        super().__init__(parent, controller, data)

        #class entry
        self.class_label = ttk.Label(self, text = 'Class (in Roman Numerals)')
        self.class_label.grid(row = 1, column = 0, columnspan = 2, sticky = 'w')
        self.class_entry = ttk.Entry(self)
        self.class_entry.grid(row = 1, column = 2)

        #quantity entry
        self.quantity_label = ttk.Label(self, text = 'Quantity')
        self.quantity_label.grid(row = 2, column = 0, sticky = 'w')
        self.quantity_entry = ttk.Entry(self)
        self.quantity_entry.grid(row = 2, column = 2)

        #output button
        roll_button = ttk.Button(self, text = 'Roll Loot', command = lambda: self.get_output())
        roll_button.grid(row = 3, column = 0, sticky = 'nsew')

    def get_output(self):
        class_var = f'Class {self.class_entry.get()}'
        quantity = int(self.quantity_entry.get())
        self.output_box.insert(tk.END, f'{quantity} x {class_var}')
        for i in range(quantity):
            mag_item = choice(list(self.data[class_var].keys()))
            if self.data[class_var][mag_item]['Cursed'] == 'Y':
                self.output_box.insert(tk.END, f'   {self.data[class_var][mag_item]['Name']}(CURSED)')
            else:
                self.output_box.insert(tk.END, f'   {self.data[class_var][mag_item]['Name']}')

class ParcelPage(BasePage):
    def __init__(self, parent, controller, data):
        super().__init__(parent, controller, data)

        #level entry
        level_label = ttk.Label(self, text = 'Party Level')
        level_label.grid(row = 1, column = 0, sticky = 'w')
        self.level_entry = ttk.Entry(self)
        self.level_entry.grid(row = 1, column = 2)

        #party size entry
        ps_label = ttk.Label(self, text = 'Party Size')
        ps_label.grid(row = 2, column = 0, sticky = 'w')
        self.ps_entry = ttk.Entry(self)
        self.ps_entry.grid(row = 2, column = 2)

        #output button
        roll_button = ttk.Button(self, text = 'Roll Loot', command = lambda: self.get_output())
        roll_button.grid(row = 3, column = 0, sticky = 'nsew')

    def add_parcels(self, lvl, size, gp = 0, items = None):
        if items == None:
            items = []
        if 0 < size <= 6:
            for i in range(size):
                gp += PARCELS[lvl][i+1]['gp']
                items.extend(PARCELS[lvl][i+1]['items'])
            return gp, items
        elif size > 6:
            for i in range(6):
                gp += PARCELS[lvl][i+1]['gp']
                items.extend(PARCELS[lvl][i+1]['items'])
            tot_gp, tot_items = self.add_parcels(lvl, size - 6, gp = gp, items = items)
            return tot_gp, tot_items

    def get_output(self):
        size = int(self.ps_entry.get())
        lvl = int(self.level_entry.get())
        gp, items = self.add_parcels(lvl, size)
        item_counts = Counter(items)

        self.output_box.insert(tk.END, f'{gp}gp')
        for class_var, num in item_counts.items():
            self.output_box.insert(tk.END, f'{num} x {class_var}')
            for i in range(num):
                mag_item = choice(list(self.data[class_var].keys()))
                if self.data[class_var][mag_item]['Cursed'] == 'Y':
                    self.output_box.insert(tk.END, f'   {self.data[class_var][mag_item]['Name']}(CURSED)')
                else:
                    self.output_box.insert(tk.END, f'   {self.data[class_var][mag_item]['Name']}')
