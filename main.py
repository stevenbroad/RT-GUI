import tkinter as tk
from tkinter import filedialog as fd, ttk, Tk

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
        self.button = ttk.Button(self, text='...', command=self.callback, width=2)
        self.button.grid(column=2,row=0)

    def callback(self):
        self.contents.set(fd.askopenfilename(filetypes=self.filetypes))
    
    def get_file_path(self):
        return self.contents.get()

class RTMainWindow(Tk):
    def __init__(self):
        super().__init__(screenName='RTMainWindow', baseName='RTMainWindow', className='RTMainWindow')
        self.title('PLEXOS Techno-economic Roundtrip Study')
        frm = ttk.Frame(self, padding=10)
        frm.grid()
        self.exec_log = tk.StringVar()
        self.config_json = FilePicker(frm, 'Round Trip Config', [('JSON File','*.json')])
        self.config_json.grid(row=0)
        self.config_json = FilePicker(frm, 'My Test', [('PLEXOS .xml','*.xml')])
        self.config_json.grid(row=2)

        btnfrm = ttk.Frame(frm)
        btnfrm.grid(row=1)
        self.launch = ttk.Button(btnfrm, text='Execute')
        self.launch.grid(column=0,row=1)
        self.edit = ttk.Button(btnfrm, text='Edit')
        self.edit.grid(column=1,row=1)
        self.cancel = ttk.Button(btnfrm, text='Cancel')
        self.cancel.grid(column=2,row=1)
        # self.log = ttk.Text(frm)
        # self.log['textvariable'] = self.exec_log
        # self.exec_log.set('Test')



    
def main():
    root = RTMainWindow()
    root.mainloop()

if __name__=='__main__':
    main()