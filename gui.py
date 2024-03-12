from tkinter import *
from tkinter.ttk import *

import logic, utils


class GUI():
    def row_doubleclick_action(self, event):
        selected = event.widget.focus()
        values = event.widget.item(selected, 'values')
        nip = values[0]
        logic.toggle_contacted_state(nip)
        self.refresh_table()

    def row_lmbclick_action(self, event):
        selected = event.widget.focus()
        values = event.widget.item(selected, 'values')

        self.entry_nip.configure(state="enabled")
        self.entry_nazwa.configure(state="enabled")
        self.entry_email.configure(state="enabled")
        self.entry_telefon.configure(state="enabled")

        self.entry_nip.delete(0, END)
        self.entry_nazwa.delete(0, END)
        self.entry_email.delete(0, END)
        self.entry_telefon.delete(0, END)

        self.entry_nip.insert(0, values[0])
        self.entry_nazwa.insert(0, values[1])
        self.entry_email.insert(0, values[2])
        self.entry_telefon.insert(0, values[3])

        self.entry_nip.configure(state="disabled")
        self.entry_nazwa.configure(state="disabled")
        self.entry_email.configure(state="disabled")
        self.entry_telefon.configure(state="disabled")

    def refresh_table(self):
        companies = logic.get_all_companies(self.config.db_engine)
        # Insert company data into the treeview
        for company in companies:
            # Insert each company record into the treeview
            entry = utils.company_to_tuple(company)
            self.table.insert(parent='', index='end', values=entry)

    def __init__(self, config):
        self.config = config
        self.root = Tk() 

        # Create a frame to hold the treeview and scrollbar
        self.frame = Frame(self.root)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.pack(fill='both', expand=True)
        
        # Create a treeview
        self.table = Treeview(self.frame)
        self.table.column("#0", width=0, stretch=False)
        self.table["columns"] = ["NIP", "Nazwa", "e-mail", "telefon", "\"Obdzwoniona\""]
        self.table["show"] = "headings"
        
        # Set column names, widths, headings
        self.table.column("\"Obdzwoniona\"", width=120, stretch=False)
        self.table.heading("\"Obdzwoniona\"", text="\"Obdzwoniona\"")
        for column in self.table["columns"][:-1]:
            self.table.column(column, width=120, stretch=True)
            self.table.heading(column, text=column)
        
        self.table.bind("<Double-1>", self.row_doubleclick_action)
        self.table.bind("<ButtonRelease-1>", self.row_lmbclick_action)
        
        # Pack the treeview into the frame
        self.table.pack(fill='both', expand=True, side='left', padx=10, pady=10)
        
        # Create a scrollbar for the treeview
        sbar = Scrollbar(self.frame, orient='vertical', command=self.table.yview)
        sbar.pack(fill='y', side='right', padx=10, pady=10)
        # Configure the scrollbar to show the full extent of the treeview
        self.table.configure(yscrollcommand=sbar.set)
        
        self.textfields_frame = Frame(self.root)
        self.textfields_frame.columnconfigure(0, weight=1)
        self.textfields_frame.rowconfigure(0, weight=1)
        self.textfields_frame.pack(fill='none', anchor='w', expand=True, padx=10)
        
        self.label_nip = Label(self.textfields_frame, text="NIP:")
        self.label_nazwa = Label(self.textfields_frame, text="Nazwa:")
        self.label_email = Label(self.textfields_frame, text="e-mail:")
        self.label_telefon = Label(self.textfields_frame, text="Telefon:")
        
        self.entry_nip = Entry(self.textfields_frame, state=DISABLED)
        self.entry_nazwa = Entry(self.textfields_frame, state=DISABLED)
        self.entry_email = Entry(self.textfields_frame, state=DISABLED)
        self.entry_telefon = Entry(self.textfields_frame, state=DISABLED)
        
        self.label_nip.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.label_nazwa.grid(row=1, column=3, padx=5, pady=5, sticky='w')
        self.label_email.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.label_telefon.grid(row=2, column=3, padx=5, pady=5, sticky='w')
        
        self.entry_nip.grid(row=1, column=2, padx=5, pady=5, sticky='w')
        self.entry_nazwa.grid(row=1, column=4, padx=5, pady=5, sticky='w')
        self.entry_email.grid(row=2, column=2, padx=5, pady=5, sticky='w')
        self.entry_telefon.grid(row=2, column=4, padx=5, pady=5, sticky='w')
        
        self.buttons_frame = Frame(self.root)
        self.buttons_frame.columnconfigure(0, weight=1)
        self.buttons_frame.rowconfigure(0, weight=1)
        self.buttons_frame.pack(fill='none', anchor='w', expand=True, padx=10)
        
        self.button_edit = Button(self.buttons_frame, text="Aktualizuj podmioty", command=logic.update_database(self.config.db_engine))  # TODO: invalid variable name
        # button_edit = Button(buttons_frame, text="Edit", command=lambda: toggle_entry_state(NORMAL))
        self.button_save = Button(self.buttons_frame, text="Zmień status")  # TODO: invalid variable name
        # button_save = Button(buttons_frame, text="Save", command=save_data)
        
        self.button_edit.grid(row=3, column=1, pady=10, sticky='w')
        self.button_save.grid(row=3, column=2, pady=10, padx=10, sticky='w')
        
        self.refresh_table()
        
        # Set the root window geometry to empty to allow it to resize automatically
        self.root.geometry('')
        # Run the GUI
        print("Starting graphical user interface.")
        self.root.mainloop()
        print("Main window closed.")
