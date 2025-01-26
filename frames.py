import tkinter as tk
from tkinter import ttk

class BasePage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.columnconfigure(3, weight = 1)
        self.rowconfigure(3, weight = 1)

        #page navigation
        cr_button = ttk.Button(self, text = 'Treasure by CR', command = lambda: controller.show_frame(EncounterPage))
        cr_button.grid(row = 0, column = 0)
        item_button = ttk.Button(self, text = 'Random Items by Class', command = lambda: controller.show_frame(ItemPage))
        item_button.grid(row = 0, column = 1)
        dragon_button = ttk.Button(self, text = 'Dragon Hoard', command = lambda: controller.show_frame(DragonPage))
        dragon_button.grid(row = 0, column = 2)

        #output box
        self.output_box = tk.Listbox(width = 175)
        self.output_box.grid(row = 0, column = 3, rowspan = 4, sticky = 'nsew' )

class EncounterPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        cr_label = ttk.Label(self, text = 'Chalenge Rating')
        cr_label.grid(row = 1, column = 0)

class ItemPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        class_label = ttk.Label(self, text = 'Class')
        class_label.grid(row = 1, column = 0)
        quantity_label = ttk.Label(self, text = 'Quantity')
        quantity_label.grid(row = 2, column = 0)

class DragonPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        age_label = ttk.Label(self, text = 'Dragon Age')
        age_label.grid(row = 1, column = 0)