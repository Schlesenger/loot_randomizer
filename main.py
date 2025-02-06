from support import*
from os.path import join
from frames import*
import textwrap

class Generator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Loot Generator')
        self.rowconfigure(0, weight = 1)
        self.columnconfigure((1), weight = 1)

        #output frame
        self.output_frame = ttk.Frame(self)
        self.output_frame.grid(row = 0, column = 1, sticky = 'nsew')
        self.output_frame.rowconfigure(0, weight = 1)
        self.output_frame.columnconfigure(0, weight = 1)
        self.output_box = tk.Listbox(self.output_frame)
        self.output_box.grid(row = 0, column = 0, sticky = 'nsew')
        self.output_box.bind('<Button-3>', self.popup_description)

        #import data
        self.magic_items = ods_to_dict(join('data', 'Magic Item Classifications.ods'))

        self.container = ttk.Frame(self)
        self.container.grid(row = 0, column = 0, sticky = 'nsew')

        self.frames = {}
        for F in (EncounterPage, ItemPage, ParcelPage):
            frame = F(self.container, self, self.magic_items)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky = 'nsew')
        
        self.show_frame(EncounterPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
    
    def search_in_dict(self, dict, target):
        for key, value in dict.items():
            k = key
            for inner_value in value.values():
                for final_value in inner_value.values():
                    if final_value == target:
                        return k
        return None
    
    def popup_description(self, event):
        try:
            index = self.output_box.curselection()[0]
            item = self.output_box.get(index).lstrip().split('(CURSED)')[0]
            popup = tk.Toplevel(self)
            popup.title(f'{item}')
            tier = self.search_in_dict(self.magic_items, item)
            if tier:
                attunment = ttk.Label(popup, text = f'Attunement: {self.magic_items[tier][item]["Attunment"]}')
                attunment.grid(row = 0, column = 0)
                price = ttk.Label(popup, text = f'Price: {self.magic_items[tier][item]["Price"]}')
                price.grid(row = 0, column = 1)
                description = ttk.Label(popup, text = textwrap.fill(f'{self.magic_items[tier][item]["Description"]}', width = 100))
                description.grid(row = 1, column = 0, columnspan = 2)
                if self.magic_items[tier][item]["Cursed"] == 'Y':
                    curse = ttk.Label(popup, text = textwrap.fill(f'CURSED: {self.magic_items[tier][item]["Curse"]}', width = 100)) 
                    curse.grid(row = 2, column = 0, columnspan = 2)       
        except IndexError:
            pass

if __name__ == '__main__':
    generator = Generator()
    generator.mainloop()