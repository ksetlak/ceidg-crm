from tkinter import *
from tkinter.ttk import *
from tkinter import Label as LegacyLabel
from tkinter import Entry as LegacyEntry

import logic, utils


class GUI:
    def row_doubleclick_action(self, event):
        selected = event.widget.focus()
        values = event.widget.item(selected, 'values')
        nip = values[0]
        logic.toggle_contacted_state(self.config.db_engine, nip)
        self.refresh_table()

    def row_lmbclick_action(self, event):
        selected = event.widget.focus()
        values = event.widget.item(selected, 'values')
        nip = values[0]
        self.selected_company = logic.get_company_by_nip(self.config.db_engine, nip)

        self.entry_nip.configure(state="normal")
        self.entry_nazwa.configure(state="normal")
        self.entry_email.configure(state="normal")
        self.entry_telefon.configure(state="normal")

        self.entry_nip.delete(0, END)
        self.entry_nazwa.delete(0, END)
        self.entry_email.delete(0, END)
        self.entry_telefon.delete(0, END)

        self.entry_nip.insert(0, values[0])
        self.entry_nazwa.insert(0, values[1])
        self.entry_email.insert(0, values[2])
        self.entry_telefon.insert(0, values[3])

        self.entry_nip.configure(state="readonly", background="#fff", readonlybackground="#fff")
        self.entry_nazwa.configure(state="readonly", background="#fff", readonlybackground="#fff")
        self.entry_email.configure(state="readonly", background="#fff", readonlybackground="#fff")
        self.entry_telefon.configure(state="readonly", background="#fff", readonlybackground="#fff")

    def button_update_command(self):
        self.label_info.configure(text="POBIERANIE NOWYCH PODMIOTÓW"); self.label_info.update()
        try:
            logic.update_database(self.config)
            self.label_info.configure(text="AKTUALIZOWANIE DANYCH KONTAKTOWYCH"); self.label_info.update()
            logic.update_contact_info(self.config)
            self.label_info.configure(text=""); self.label_info.update()
        except Exception as e:  # TODO Can we narrow this clause down? (IndexError for sure)
            self.label_info.configure(text="BŁĄD!!!"); self.label_info.update()
            print(repr(e))
        self.refresh_table()

    def button_toggle_company_command(self):
        nip = self.selected_company.nip
        logic.toggle_contacted_state(self.config.db_engine, nip)
        self.refresh_table()

    def button_view_company_details_command(self):
        utils.view_company_in_browser(self.selected_company.uuid)

    def refresh_table(self):
        self.table.delete(*self.table.get_children())
        companies = logic.get_companies_with_contact_data(self.config.db_engine)
        # Insert company data into the treeview
        for company in companies:
            # Insert each company record into the treeview
            entry = utils.company_to_tuple(company)
            self.table.insert(parent='', index='end', values=entry)

    def show_context_menu(self, event):
        self.context_menu.tk_popup(event.x_root, event.y_root)

    def __init__(self, config):
        self.config = config
        self.root = Tk()
        self.selected_company = None

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
        
        self.entry_nip = LegacyEntry(self.textfields_frame, state=DISABLED)
        self.entry_nazwa = LegacyEntry(self.textfields_frame, width=50, state=DISABLED)
        self.entry_email = LegacyEntry(self.textfields_frame, state=DISABLED)
        self.entry_telefon = LegacyEntry(self.textfields_frame, width=50, state=DISABLED)
        
        self.label_nip.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.label_nazwa.grid(row=1, column=3, padx=5, pady=5, sticky='w')
        self.label_email.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.label_telefon.grid(row=2, column=3, padx=5, pady=5, sticky='w')
        
        self.entry_nip.grid(row=1, column=2, padx=5, pady=5, sticky='w')
        self.entry_nazwa.grid(row=1, column=4, padx=5, pady=5, sticky='w')
        self.entry_email.grid(row=2, column=2, padx=5, pady=5, sticky='w')
        self.entry_telefon.grid(row=2, column=4, padx=5, pady=5, sticky='w')
        
        self.label_info = LegacyLabel(self.textfields_frame, text="", fg='#f00', font=("bold", 25))
        self.label_info.grid(row=1, column=5, padx=20, pady=5, sticky='w')

        self.buttons_frame = Frame(self.root)
        self.buttons_frame.columnconfigure(0, weight=1)
        self.buttons_frame.rowconfigure(0, weight=1)
        self.buttons_frame.pack(fill='none', anchor='w', expand=True, padx=10)
        
        self.context_menu = Menu(self.root, tearoff=False)
        self.context_menu.add_command(label="Użyj Ctrl+C, aby skopiować.")
        self.entry_nip.bind("<Button-3>", self.show_context_menu)
        self.entry_nazwa.bind("<Button-3>", self.show_context_menu)
        self.entry_email.bind("<Button-3>", self.show_context_menu)
        self.entry_telefon.bind("<Button-3>", self.show_context_menu)

        self.button_update = Button(self.buttons_frame, text="Aktualizuj podmioty", command=self.button_update_command)
        self.button_toggle_company = Button(self.buttons_frame, text="Zmień status", command=self.button_toggle_company_command)
        self.button_view_company_details = Button(self.buttons_frame, text="Szczegóły", command=self.button_view_company_details_command)

        self.button_update.grid(row=3, column=1, pady=10, padx=10, sticky='sw')
        self.button_toggle_company.grid(row=3, column=2, pady=10, padx=10, sticky='sw')
        self.button_view_company_details.grid(row=3, column=3, pady=10, padx=10, sticky='sw')
        
        self.refresh_table()
        
        # Set the root window geometry to empty to allow it to resize automatically.
        self.root.geometry("1400x700")
        self.root.mainloop()
