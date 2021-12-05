import os, json
import tkinter as tk
from tkinter import filedialog as fd, ttk, Tk, scrolledtext as st
from tkinter.constants import END

class FilePicker(tk.Frame):
    def __init__(self, master, label, filetypes):
        super().__init__(master=master)
        self.grid()
        self.contents = tk.StringVar()
        self.filetypes = filetypes
        self.label = ttk.Label(self, text=label, width=20)
        self.label.grid(column=0,row=0)
        self.entry = ttk.Entry(self, text='', width=100)
        self.entry.grid(column=1,row=0)
        self.entry['textvariable'] = self.contents
        self.choose_file_btn = ttk.Button(self, text='...', command=self.select_file, width=2)
        self.choose_file_btn.grid(column=2,row=0)
        self.create_file_btn = ttk.Button(self, text='+', command=self.create_file, width=2)
        self.create_file_btn.grid(column=3,row=0)

    def select_file(self):
        self.contents.set(fd.askopenfilename(filetypes=self.filetypes))
    
    def create_file(self):
        self.contents.set(fd.asksaveasfilename(filetypes=self.filetypes))
        with open(self.get_file_path(), 'w') as fp:
            json.dump({}, fp)
    
    def get_file_path(self):
        return self.contents.get()

    def get_value(self):
        return self.get_file_path()

    def set_value(self, value):
        self.contents.set(value)

class ButtonRow(tk.Frame):
    def __init__(self, master, *buttons):
        super().__init__(master=master)
        self.buttons = [ttk.Button(self, text=label, command=action) for label, action in buttons]
        for idx, btn in enumerate(self.buttons):
            btn.grid(column=idx, row=0)

class RTEditWindow(Tk):
    def __init__(self, config_file, log_message):
        super().__init__()
        self.title('Edit/Verify ' + config_file)
        frm = ttk.Frame(self)
        frm.grid()
        log_message('**Editing {}', config_file)
        self.config_file = config_file
    
class RTMainWindow(Tk):
    def __init__(self):
        super().__init__()
        self.title('PLEXOS Techno-economic Roundtrip Study')
        frm = ttk.Frame(self, padding=10)
        frm.grid()
        self.config_json = FilePicker(frm, 'Round Trip Config', [('JSON File','*.json')])

        ButtonRow(frm, ('Save', self.save_config), ('Revert', self.load_config), ('Cancel', self.destroy)).grid(row=1)
        self.inputs = {
            'plx_input': FilePicker(frm, 'PLEXOS Input', [('PLEXOS Input .xml', '*.xml')]),
            'psse_sav': FilePicker(frm, 'PSS/E Sav File', [('PSS/E .sav', '*.sav')]),
            'psse_mon': FilePicker(frm, 'PSS/E Mon File', [('PSS/E .mon', '*.mon')]),
            'psse_con': FilePicker(frm, 'PSS/E Con File', [('PSS/E .con', '*.con')]),
            'psse_dfx': FilePicker(frm, 'PSS/E Distribution File', [('PSS/E .dfx', '*.dfx')])
        }

        ButtonRow(frm, ('Execute',self.execute_roundtrip), ('Edit', self.edit_rtconfig), ('Cancel', self.destroy)).grid(row=2+len(self.inputs))

        self.log = st.ScrolledText(frm)
        self.log.grid(row=3+len(self.inputs))
        self.log.insert(END, '*'*25)

        ButtonRow(frm, ('Open PLEXOS', None), ('Open PSS/E', None), ('Open Logfile', None)).grid(row=4+len(self.inputs))
    
    def save_config(self):
        jobj = {}
        for key, fld in self.inputs.items():
            jobj[key] = fld.get_value()
        json.dump(jobj, open(self.config_json.get_value(), 'w'))

    def load_value(self, key, value):
        if key in self.inputs:
            self.inputs[key].set_value(value)

    def load_config(self):
        jobj = json.load(open(self.config_json.get_value()))
        for key, value in jobj.items():
            self.load_value(key, value)

    def log_message(self, fmt, *args, **kargs):
        self.log.insert(END, '\n' + fmt.format(*args, **kargs))

    def execute_roundtrip(self):
        if not os.path.exists(self.config_json.get_file_path()):
            self.edit_rtconfig()
        else:
            self.log_message('*****{}*****', self.config_json.get_file_path())
            self.config_jobj = json.load(open(self.config_json.get_file_path()))
            self.log_message('{}', json.dumps(self.config_jobj)[:1000])

    def edit_rtconfig(self):
        RTEditWindow(self.config_json.get_file_path(), self.log_message).mainloop()



    
def main():
    root = RTMainWindow()
    root.mainloop()

if __name__=='__main__':
    main()