from support import*
from os.path import join
from frames import*

class Generator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Loot Generator')
        self.rowconfigure(0, weight = 1)
        self.columnconfigure(0, weight = 1)

        container = ttk.Frame(self)
        container.grid(row = 0, column = 0, sticky = 'nsew')

        self.frames = {}
        for F in (EncounterPage, ItemPage, DragonPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky = 'nsew')
        
        self.show_frame(EncounterPage)

        #import data
        self.data = ods_to_dict(join('data', 'Magic Item Classifications.ods'))

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

if __name__ == '__main__':
    generator = Generator()
    generator.mainloop()