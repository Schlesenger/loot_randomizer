from support import*
from os.path import join
from frames import*

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

        #import data
        self.magic_items = ods_to_dict(join('data', 'Magic Item Classifications.ods'))

        self.container = ttk.Frame(self)
        self.container.grid(row = 0, column = 0, sticky = 'nsew')

        self.frames = {}
        for F in (EncounterPage, ItemPage, DragonPage):
            frame = F(self.container, self, self.magic_items)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky = 'nsew')
        
        self.show_frame(EncounterPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

if __name__ == '__main__':
    generator = Generator()
    generator.mainloop()