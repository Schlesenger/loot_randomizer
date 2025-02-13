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
        self.clear_button.grid(row = 4, column = 1, sticky = 'nsew')

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
        roll_button.grid(row = 4, column = 0, sticky = 'nsew')

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
                                self.output_box.insert(tk.END, f'    {count}x{value}')
                            self.output_box.insert(tk.END, f'  Total gp value of {total_gold + (object_num * 10)}gp')
                            
                        case '50 gp gems':
                            self.output_box.insert(tk.END, f'{object_num}x{object}')
                            list_of_gems = []
                            for i in range(object_num):
                                list_of_gems.append(randint(1, 12))
                            set_of_gems = set(list_of_gems)
                            for key in set_of_gems:
                                value = GEMSTONES[object][key]
                                count = list_of_gems.count(key)
                                self.output_box.insert(tk.END, f'    {count}x{value}')
                            self.output_box.insert(tk.END, f'  Total gp value of {total_gold + (object_num * 50)}gp')

                        case '25 gp art objects':
                            self.output_box.insert(tk.END, f'{object_num}x{object}')
                            list_of_art = []
                            for i in range(object_num):
                                list_of_art.append(randint(1, 10))
                            set_of_art = set(list_of_art)
                            for key in set_of_art:
                                value = ARTPIECES[object][key]
                                count = list_of_art.count(key)
                                self.output_box.insert(tk.END, f'    {count}x{value}')
                            self.output_box.insert(tk.END, f'  Total gp value of {total_gold + (object_num * 25)}gp')

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
                                self.output_box.insert(tk.END, f'    {count}x{value}')
                            self.output_box.insert(tk.END, f'  Total gp value of {total_gold + (object_num * 50)}gp')

                        case '100 gp gems':
                            self.output_box.insert(tk.END, f'{object_num}x{object}')
                            list_of_gems = []
                            for i in range(object_num):
                                list_of_gems.append(randint(1, 10))
                            set_of_gems = set(list_of_gems)
                            for key in set_of_gems:
                                value = GEMSTONES[object][key]
                                count = list_of_gems.count(key)
                                self.output_box.insert(tk.END, f'    {count}x{value}')
                            self.output_box.insert(tk.END, f'  Total gp value of {total_gold + (object_num * 100)}gp')

                        case '25 gp art objects':
                            self.output_box.insert(tk.END, f'{object_num}x{object}')
                            list_of_art = []
                            for i in range(object_num):
                                list_of_art.append(randint(1, 10))
                            set_of_art = set(list_of_art)
                            for key in set_of_art:
                                value = ARTPIECES[object][key]
                                count = list_of_art.count(key)
                                self.output_box.insert(tk.END, f'    {count}x{value}')
                            self.output_box.insert(tk.END, f'  Total gp value of {total_gold + (object_num * 25)}gp')

                        case '250 gp art objects':
                            self.output_box.insert(tk.END, f'{object_num}x{object}')
                            list_of_gems = []
                            for i in range(object_num):
                                list_of_gems.append(randint(1, 10))
                            set_of_gems = set(list_of_gems)
                            for key in set_of_gems:
                                value = ARTPIECES[object][key]
                                count = list_of_gems.count(key)
                                self.output_box.insert(tk.END, f'    {count}x{value}')
                            self.output_box.insert(tk.END, f'  Total gp value of {total_gold + (object_num * 250)}gp')

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
                                self.output_box.insert(tk.END, f'    {count}x{value}')
                            self.output_box.insert(tk.END, f'  Total gp value of {total_gold + (object_num * 500)}gp')

                        case '1000 gp gems':
                            self.output_box.insert(tk.END, f'{object_num}x{object}')
                            list_of_gems = []
                            for i in range(object_num):
                                list_of_gems.append(randint(1, 8))
                            set_of_gems = set(list_of_gems)
                            for key in set_of_gems:
                                value = GEMSTONES[object][key]
                                count = list_of_gems.count(key)
                                self.output_box.insert(tk.END, f'    {count}x{value}')
                            self.output_box.insert(tk.END, f'  Total gp value of {total_gold + (object_num * 100)}gp')

                        case '250 gp art objects':
                            self.output_box.insert(tk.END, f'{object_num}x{object}')
                            list_of_art = []
                            for i in range(object_num):
                                list_of_art.append(randint(1, 10))
                            set_of_art = set(list_of_art)
                            for key in set_of_art:
                                value = ARTPIECES[object][key]
                                count = list_of_art.count(key)
                                self.output_box.insert(tk.END, f'    {count}x{value}')
                            self.output_box.insert(tk.END, f'  Total gp value of {total_gold + (object_num * 250)}gp')

                        case '750 gp art objects':
                            self.output_box.insert(tk.END, f'{object_num}x{object}')
                            list_of_gems = []
                            for i in range(object_num):
                                list_of_gems.append(randint(1, 10))
                            set_of_gems = set(list_of_gems)
                            for key in set_of_gems:
                                value = ARTPIECES[object][key]
                                count = list_of_gems.count(key)
                                self.output_box.insert(tk.END, f'    {count}x{value}')
                            self.output_box.insert(tk.END, f'  Total gp value of {total_gold + (object_num * 750)}gp')

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
                                self.output_box.insert(tk.END, f'    {count}x{value}')
                            self.output_box.insert(tk.END, f'  Total gp value of {total_gold + (object_num * 1000)}gp')

                        case '5000 gp gems':
                            self.output_box.insert(tk.END, f'{object_num}x{object}')
                            list_of_gems = []
                            for i in range(object_num):
                                list_of_gems.append(randint(1, 4))
                            set_of_gems = set(list_of_gems)
                            for key in set_of_gems:
                                value = GEMSTONES[object][key]
                                count = list_of_gems.count(key)
                                self.output_box.insert(tk.END, f'    {count}x{value}')
                            self.output_box.insert(tk.END, f'  Total gp value of {total_gold + (object_num * 5000)}gp')

                        case '2500 gp art objects':
                            self.output_box.insert(tk.END, f'{object_num}x{object}')
                            list_of_art = []
                            for i in range(object_num):
                                list_of_art.append(randint(1, 10))
                            set_of_art = set(list_of_art)
                            for key in set_of_art:
                                value = ARTPIECES[object][key]
                                count = list_of_art.count(key)
                                self.output_box.insert(tk.END, f'    {count}x{value}')
                            self.output_box.insert(tk.END, f'  Total gp value of {total_gold + (object_num * 2500)}gp')

                        case '7500 gp art objects':
                            self.output_box.insert(tk.END, f'{object_num}x{object}')
                            list_of_gems = []
                            for i in range(object_num):
                                list_of_gems.append(randint(1, 8))
                            set_of_gems = set(list_of_gems)
                            for key in set_of_gems:
                                value = ARTPIECES[object][key]
                                count = list_of_gems.count(key)
                                self.output_box.insert(tk.END, f'    {count}x{value}')
                            self.output_box.insert(tk.END, f'  Total gp value of {total_gold + (object_num * 7500)}gp')

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
        roll_button.grid(row = 4, column = 0, sticky = 'nsew')

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

        #parcel size entry
        parcel_label = ttk.Label(self, text = 'Number of Parcels')
        parcel_label.grid(row = 3, column = 0, columnspan = 2, sticky = 'w')
        self.parcel_entry = ttk.Entry(self)
        self.parcel_entry.grid(row = 3, column = 2)

        #output button
        roll_button = ttk.Button(self, text = 'Roll Loot', command = lambda: self.get_output())
        roll_button.grid(row = 4, column = 0, sticky = 'nsew')

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
    
    def make_parcels(self, gp, items, parcels):
        list_container = []
        gp_low = gp // (parcels + 1)
        gp_high = gp // (parcels - 1)
        for i in range(parcels):
            list_container.append([])
        for list in list_container:
            input_gp = randint(gp_low, gp_high)
            if input_gp >= gp:
                list.append(gp)
                gp -= gp
            else:
                list.append(input_gp)
                gp -= input_gp
        for item in items:
            parcel = randint(0, parcels - 1)
            list_container[parcel].append(item)
        return list_container

    def get_output(self):
        size = int(self.ps_entry.get())
        lvl = int(self.level_entry.get())
        parcels = int(self.parcel_entry.get())
        gp, items = self.add_parcels(lvl, size)
        parcel_container = self.make_parcels(gp, items, parcels)
        parcel_num = 1
        
        for parcel in parcel_container:
            self.output_box.insert(tk.END, f'Parcel #{parcel_num}')
            parcel_num += 1

            #printing total amount for parcel
            parcel_gold = parcel.pop(0)
            item_counts = Counter(parcel)
            item_set = set(parcel)
            string_var = f'   Total {parcel_gold}gp'
            for item in item_set:
                string_var += f', {item_counts[item]} x {item}'
            self.output_box.insert(tk.END, string_var)

            #printing mundane items
            match parcel_gold:
                case num if 0 <= num < 1000:
                    obj_num = self.roll_dice(2, 6)
                    obj_list = []
                    for i in range(obj_num):
                        obj_list.append(choice(['10 gp gems', '25 gp art objects', '50 gp gems']))
                    obj_count = Counter(obj_list)

                    for obj, count in obj_count.items():
                        match obj:
                            case '10 gp gems':
                                if parcel_gold >= count * 10:
                                    parcel_gold -= count * 10
                                    list_of_obj = []
                                    for i in range(count):
                                        list_of_obj.append(randint(1, 12))
                                    set_of_obj = set(list_of_obj)
                                    for key in set_of_obj:
                                        value = GEMSTONES[obj][key]
                                        value_count = list_of_obj.count(key)
                                        self.output_box.insert(tk.END, f'      {value_count}x{value} (10gp each)')

                            case '50 gp gems':
                                if parcel_gold >= count * 50:
                                    parcel_gold -= count * 50
                                    list_of_obj = []
                                    for i in range(count):
                                        list_of_obj.append(randint(1, 12))
                                    set_of_obj = set(list_of_obj)
                                    for key in set_of_obj:
                                        value = GEMSTONES[obj][key]
                                        value_count = list_of_obj.count(key)
                                        self.output_box.insert(tk.END, f'      {value_count}x{value} (50gp each)')

                            case '25 gp art objects':
                                if parcel_gold >= count * 25:
                                    parcel_gold -= count * 25
                                    list_of_obj = []
                                    for i in range(obj_num):
                                        list_of_obj.append(randint(1, 10))
                                    set_of_obj = set(list_of_obj)
                                    for key in set_of_obj:
                                        value = ARTPIECES[obj][key]
                                        value_count = list_of_obj.count(key)
                                        self.output_box.insert(tk.END, f'      {value_count}x{value} (25gp each)')
                    self.output_box.insert(tk.END, f'      {parcel_gold}gp')

                case num if 1000 <= num < 4000:
                    obj_num = self.roll_dice(2, 6)
                    obj_list = []
                    for i in range(obj_num):
                        obj_list.append(choice(['25 gp art objects', '250 gp art objects', '50 gp gems', '100 gp gems']))
                    obj_count = Counter(obj_list)

                    for obj, count in obj_count.items():
                        match obj:
                            case '50 gp gems':
                                if parcel_gold >= count * 50:
                                    parcel_gold -= count * 50
                                    list_of_obj = []
                                    for i in range(count):
                                        list_of_obj.append(randint(1, 12))
                                    set_of_obj = set(list_of_obj)
                                    for key in set_of_obj:
                                        value = GEMSTONES[obj][key]
                                        value_count = list_of_obj.count(key)
                                        self.output_box.insert(tk.END, f'      {value_count}x{value} (50gp each)')

                            case '100 gp gems':
                                if parcel_gold >= count * 100:
                                    parcel_gold -= count * 100
                                    list_of_obj = []
                                    for i in range(count):
                                        list_of_obj.append(randint(1, 10))
                                    set_of_obj = set(list_of_obj)
                                    for key in set_of_obj:
                                        value = GEMSTONES[obj][key]
                                        value_count = list_of_obj.count(key)
                                        self.output_box.insert(tk.END, f'      {value_count}x{value} (100gp each)')

                            case '25 gp art objects':
                                if parcel_gold >= count * 25:
                                    parcel_gold -= count * 25
                                    list_of_obj = []
                                    for i in range(count):
                                        list_of_obj.append(randint(1, 10))
                                    set_of_obj = set(list_of_obj)
                                    for key in set_of_obj:
                                        value = ARTPIECES[obj][key]
                                        value_count = list_of_obj.count(key)
                                        self.output_box.insert(tk.END, f'      {value_count}x{value} (25gp each)')

                            case '250 gp art objects':
                                if parcel_gold >= count * 250:
                                    parcel_gold -= count * 250
                                    list_of_obj = []
                                    for i in range(count):
                                        list_of_obj.append(randint(1, 10))
                                    set_of_obj = set(list_of_obj)
                                    for key in set_of_obj:
                                        value = ARTPIECES[obj][key]
                                        value_count = list_of_obj.count(key)
                                        self.output_box.insert(tk.END, f'      {value_count}x{value} (250gp each)')
                    self.output_box.insert(tk.END, f'      {parcel_gold}gp')

                case num if 4000 <= num < 15000:
                    obj_num = self.roll_dice(2, 6)
                    obj_list = []
                    for i in range(obj_num):
                        obj_list.append(choice(['250 gp art pieces', '750 gp art pieces', '500 gp gems', '1000 gp gems']))
                    obj_count = Counter(obj_list)

                    for obj, count in obj_count.items():
                        match obj:
                            case '250 gp art objects':
                                if parcel_gold >= count * 250:
                                    parcel_gold -= count * 250
                                    list_of_obj = []
                                    for i in range(count):
                                        list_of_obj.append(randint(1, 10))
                                    set_of_obj = set(list_of_obj)
                                    for key in set_of_obj:
                                        value = ARTPIECES[obj][key]
                                        value_count = list_of_obj.count(key)
                                        self.output_box.insert(tk.END, f'      {value_count}x{value} (250gp each)')

                            case '750 gp art objects':
                                if parcel_gold >= count * 750:
                                    parcel_gold -= count * 750
                                    list_of_obj = []
                                    for i in range(count):
                                        list_of_obj.append(randint(1, 10))
                                    set_of_obj = set(list_of_obj)
                                    for key in set_of_obj:
                                        value = ARTPIECES[obj][key]
                                        value_count = list_of_obj.count(key)
                                        self.output_box.insert(tk.END, f'      {value_count}x{value} (750gp each)')

                            case '500 gp gems':
                                if parcel_gold >= count * 500:
                                    parcel_gold -= count * 500
                                    list_of_obj = []
                                    for i in range(count):
                                        list_of_obj.append(randint(1, 6))
                                    set_of_obj = set(list_of_obj)
                                    for key in set_of_obj:
                                        value = GEMSTONES[obj][key]
                                        value_count = list_of_obj.count(key)
                                        self.output_box.insert(tk.END, f'      {value_count}x{value} (500gp each)')
                                
                            case '1000 gp gems':
                                if parcel_gold >= count * 1000:
                                    parcel_gold -= count * 1000
                                    list_of_obj = []
                                    for i in range(count):
                                        list_of_obj.append(randint(1, 8))
                                    set_of_obj = set(list_of_obj)
                                    for key in set_of_obj:
                                        value = GEMSTONES[obj][key]
                                        value_count = list_of_obj.count(key)
                                        self.output_box.insert(tk.END, f'      {value_count}x{value} (1000gp each)')
                    self.output_box.insert(tk.END, f'      {parcel_gold}gp')

                case num if 15000 <= num < 60000:
                    obj_num = self.roll_dice(1, 8)
                    obj_list = []
                    for i in range(obj_num):
                        obj_list.append(choice(['1000 gp gems', '5000 gp gems', '2500 gp art objects', '7500 gp art objects']))
                    obj_count = Counter(obj_list)
                    
                    for obj, count in obj_count.items():
                        match obj:
                            case '2500 gp art objects':
                                if parcel_gold >= count * 2500:
                                    parcel_gold -= count * 2500
                                    list_of_obj = []
                                    for i in range(count):
                                        list_of_obj.append(randint(1, 10))
                                    set_of_obj = set(list_of_obj)
                                    for key in set_of_obj:
                                        value = ARTPIECES[obj][key]
                                        value_count = list_of_obj.count(key)
                                        self.output_box.insert(tk.END, f'      {value_count}x{value} (2500gp each)')

                            case '7500 gp art objects':
                                if parcel_gold >= count * 7500:
                                    parcel_gold -= count * 7500
                                    list_of_obj = []
                                    for i in range(count):
                                        list_of_obj.append(randint(1, 8))
                                    set_of_obj = set(list_of_obj)
                                    for key in set_of_obj:
                                        value = ARTPIECES[obj][key]
                                        value_count = list_of_obj.count(key)
                                        self.output_box.insert(tk.END, f'      {value_count}x{value} (7500gp each)')

                            case '1000 gp gems':
                                if parcel_gold >= count * 1000:
                                    parcel_gold -= count * 1000
                                    list_of_obj = []
                                    for i in range(count):
                                        list_of_obj.append(randint(1, 8))
                                    set_of_obj = set(list_of_obj)
                                    for key in set_of_obj:
                                        value = GEMSTONES[obj][key]
                                        value_count = list_of_obj.count(key)
                                        self.output_box.insert(tk.END, f'      {value_count}x{value} (1000gp each)')

                            case '5000 gp gems':
                                if parcel_gold >= count * 5000:
                                    parcel_gold -= count * 5000
                                    list_of_obj = []
                                    for i in range(count):
                                        list_of_obj.append(randint(1, 4))
                                    set_of_obj = set(list_of_obj)
                                    for key in set_of_obj:
                                        value = GEMSTONES[obj][key]
                                        value_count = list_of_obj.count(key)
                                        self.output_box.insert(tk.END, f'      {value_count}x{value} (5000gp each)')
                    self.output_box.insert(tk.END, f'      {parcel_gold}gp')

                case num if num >= 60000:
                    obj_num = self.roll_dice(3, 6)
                    obj_list = []
                    for i in range(obj_num):
                        obj_list.append(choice(['5000 gp gems', '7500 gp art objects']))
                    obj_count = Counter(obj_list)
                    
                    for obj, count in obj_count.items():
                        match obj:
                            case '7500 gp art objects':
                                if parcel_gold >= count * 7500:
                                    parcel_gold -= count * 7500
                                    list_of_obj = []
                                    for i in range(count):
                                        list_of_obj.append(randint(1, 8))
                                    set_of_obj = set(list_of_obj)
                                    for key in set_of_obj:
                                        value = ARTPIECES[obj][key]
                                        value_count = list_of_obj.count(key)
                                        self.output_box.insert(tk.END, f'      {value_count}x{value} (7500gp each)')

                            case '5000 gp gems':
                                if parcel_gold >= count * 5000:
                                    parcel_gold -= count * 5000
                                    list_of_obj = []
                                    for i in range(count):
                                        list_of_obj.append(randint(1, 4))
                                    set_of_obj = set(list_of_obj)
                                    for key in set_of_obj:
                                        value = GEMSTONES[obj][key]
                                        value_count = list_of_obj.count(key)
                                        self.output_box.insert(tk.END, f'      {value_count}x{value} (5000gp each)')
                    self.output_box.insert(tk.END, f'      {parcel_gold}gp')

            #printing magical items
            for item in item_set:
                self.output_box.insert(tk.END, f'   {item}')
                for i in range(item_counts[item]):
                    mag_item = choice(list(self.data[item].keys()))
                    if self.data[item][mag_item]['Cursed'] == 'Y':
                        self.output_box.insert(tk.END, f'      {self.data[item][mag_item]['Name']}(CURSED)')
                    else:
                        self.output_box.insert(tk.END, f'      {self.data[item][mag_item]['Name']}')
