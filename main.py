import os, json
import tkinter as tk
from tkinter import filedialog as fd, ttk, Tk, scrolledtext as st
from tkinter.constants import END

class FilePicker(tk.Frame):
    def __init__(self, master, label, filetypes, **options):
        super().__init__(master=master)
        self.grid()
        self.contents = tk.StringVar()
        self.filetypes = filetypes
        self.label = ttk.Label(self, text=label, width=self.get_option_value('label_width', 20, **options))
        self.label.grid(column=0,row=0)
        self.entry = ttk.Entry(self, text='', width=self.get_option_value('entry_width', 100, **options))
        self.entry.grid(column=1,row=0)
        self.entry['textvariable'] = self.contents
        self.select_action = self.get_option_value('select_action', None, **options)
        self.create_action = self.get_option_value('create_action', None, **options)
        if self.get_option_value('selectable', True, **options):
            self.choose_file_btn = ttk.Button(self, text='...', command=self.select_file, width=self.get_option_value('button_width', 2, **options))
            self.choose_file_btn.grid(column=2,row=0)
        if self.get_option_value('createable', True, **options):
            self.create_file_btn = ttk.Button(self, text='+', command=self.create_file, width=self.get_option_value('button_width', 2, **options))
            self.create_file_btn.grid(column=3,row=0)

    def get_option_value(self, option, default_value, **options):
        return default_value if not option in options else options[option]

    def select_file(self):
        self.contents.set(fd.askopenfilename(filetypes=self.filetypes))
        if not self.select_action is None:
            self.select_action()
    
    def create_file(self):
        self.contents.set(fd.asksaveasfilename(filetypes=self.filetypes))
        with open(self.get_file_path(), 'w') as fp:
            json.dump({}, fp)
        if not self.create_action is None:
            self.create_action()
    
    def get_file_path(self):
        return self.contents.get()

    def get_value(self):
        return self.get_file_path()

    def set_value(self, value):
        self.contents.set(value)

class FolderPicker(tk.Frame):
    def __init__(self, master, label, **options):
        super().__init__(master=master)
        self.grid()
        self.contents = tk.StringVar()
        self.label = ttk.Label(self, text=label, width=self.get_option_value('label_width', 20, **options))
        self.label.grid(column=0,row=0)
        self.entry = ttk.Entry(self, text='', width=self.get_option_value('entry_width', 100, **options))
        self.entry.grid(column=1,row=0)
        self.entry['textvariable'] = self.contents
        self.choose_fldr_btn = ttk.Button(self, text='...', command=self.select_folder, width=self.get_option_value('button_width', 2, **options))
        self.choose_fldr_btn.grid(column=2,row=0)

    def get_option_value(self, option, default_value, **options):
        return default_value if not option in options else options[option]

    def select_folder(self):
        self.contents.set(fd.askdirectory())

    def get_value(self):
        return self.contents.get()

    def set_value(self, value):
        self.contents.set(value)

class ButtonRow(tk.Frame):
    def __init__(self, master, *buttons):
        super().__init__(master=master)
        self.buttons = [ttk.Button(self, text=label, command=action) for label, action in buttons]
        for idx, btn in enumerate(self.buttons):
            btn.grid(column=idx, row=0)


class LabeledEntry(tk.Frame):
    def __init__(self, master, label, **options):
        super().__init__(master=master)
        self.grid()
        ttk.Label(self, text=label, width=self.get_option_value('label_width', 20, **options)).grid(row=0,column=0)
        self.content = tk.StringVar()
        self.entry = ttk.Entry(self, text=label, width=self.get_option_value('entry_width', 100, **options))
        self.entry.grid(row=0,column=1)
        self.entry['textvariable'] = self.content

    def get_option_value(self, option, default_value, **options):
        return default_value if not option in options else options[option]

    def get_value(self):
        return self.content.get()

    def set_value(self, value):
        self.content.set(value)

class RTMainWindow(Tk):
    def __init__(self):
        super().__init__()
        self.title('PLEXOS Techno-economic Roundtrip Study')
        frm = ttk.Frame(self, padding=10)
        frm.grid()
        self.config_json = FilePicker(
            frm, 'Round Trip Config', [('JSON File','*.json')],
            select_action=self.load_config,
            create_action=self.save_config
        )

        ButtonRow(frm, ('Save', self.save_config), ('Revert', self.load_config), ('Execute',self.execute_roundtrip), ('Cancel', self.destroy)).grid(row=1)
        self.inputs = {
            'plx_input': FilePicker(frm, 'PLEXOS Input', [('PLEXOS Input .xml', '*.xml')], createable=False, entry_width=103),
            'plx_model': LabeledEntry(frm, 'PLEXOS Model', entry_width=106),
            'psse_sav': FilePicker(frm, 'PSS/E Sav File', [('PSS/E .sav', '*.sav')], createable=False, entry_width=103),
            'psse_mon': FilePicker(frm, 'PSS/E Mon File', [('PSS/E .mon', '*.mon')], createable=False, entry_width=103),
            'psse_con': FilePicker(frm, 'PSS/E Con File', [('PSS/E .con', '*.con')], createable=False, entry_width=103),
            'psse_dfx': FilePicker(frm, 'PSS/E Distribution File', [('PSS/E .dfx', '*.dfx')], createable=False, entry_width=103),
            'sql_server': LabeledEntry(frm, 'SQL Server', entry_width=106),
            'sql_input': LabeledEntry(frm, 'SQL Input DB', entry_width=106),
            'sql_output': LabeledEntry(frm, 'SQL Output DB', entry_width=106),
            'script_folder': FolderPicker(frm, 'Script Folder', entry_width=103)
        }

        self.log = st.ScrolledText(frm, width=93)
        self.log.grid(row=2+len(self.inputs))
        self.log.insert(END, '*'*25)

        ButtonRow(frm, ('Open PLEXOS', None), ('Open PSS/E', None), ('Open Logfile', None)).grid(row=3+len(self.inputs))
    
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


    
def main():
    root = RTMainWindow()
    root.mainloop()

if __name__=='__main__':
    main()