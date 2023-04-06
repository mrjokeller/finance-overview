import datetime as dt
import tkinter as tk
from tkinter import ttk, messagebox
import importer
import json


def get_countries():
    with open("./countries.json", "r") as f:
        countries_dict = json.load(f)
    return countries_dict["countries"]

def add_country(country: str):
    countries = get_countries()
    countries["countries"].extend(country.lower())
    countries["countries"].sort()
    with open("./countries.json", "w") as f:
        json.dumps(countries)
    

class UI:
    
    def __init__(self, categories: dict, databases: dict):
        
        # Setup main window
        self.window = tk.Tk()
        self.window.title("Travel Expenses")
        self.window.geometry("500x500")
        self.window.minsize(500, 500)
        
        self.window.config(padx=20, pady=20)
        
        # Setup tabs
        self.tabview = ttk.Notebook(self.window, width=400, height=400)
        self.tab1 = ttk.Frame(self.tabview)
        self.tab2 = ttk.Frame(self.tabview)
        self.tab3 = ttk.Frame(self.tabview)
        self.tabview.add(self.tab1, text="Country")
        self.tabview.add(self.tab2, text="Fixed Cost")
        self.tabview.add(self.tab3, text="Income")
        self.tabview.grid(row=0, column=0, columnspan=3, sticky='nsew')
        
        # Setup of lists and dictionaries
        self.databases = databases
        self.categories = categories
        self.all_countries = get_countries()
        self.countries = databases["country"].get_selected_countries()
        if self.countries == []:
            self.add_expense_window()
        self.category_labels = {}
        
        ### Tab 1 ###
        
        self.tab1.grid_columnconfigure(0, weight=2, uniform="fred")
        self.tab1.grid_columnconfigure(1, weight=1, uniform="fred")
        self.tab1.grid_columnconfigure(2, weight=1, uniform="fred")
        
        # create a separator
        separator = ttk.Separator(self.tab1, orient='horizontal')
        separator.grid(row=2, column=0, columnspan=3, sticky='ew', pady=10)
        
        self.subheading_label = tk.Label(self.tab1, text="Categories", font=("Arial", 16))
        self.subheading_label.grid(row=1, column=0, sticky='w')
        self.subheading_label_2 = tk.Label(self.tab1, text="Actual", font=("Arial", 16))
        self.subheading_label_2.grid(row=1, column=1, sticky='e')
        self.subheading_label_3 = tk.Label(self.tab1, text="Planned", font=("Arial", 16))
        self.subheading_label_3.grid(row=1, column=2, sticky='e')
        
        # create a separator
        separator = ttk.Separator(self.tab1, orient='horizontal')
        separator.grid(row=9, column=0, columnspan=3, sticky='ew', pady=10)
        
        # Labels with total cost, total planned cost and total difference
        self.total_cost_label = tk.Label(self.tab1, text="Total:", font=("Arial", 16))
        self.total_cost_label.grid(row=10, column=0, sticky='w')
        self.total_difference_label = tk.Label(self.tab1, text="Difference: ", font=("Arial", 16))
        self.total_difference_label.grid(row=12, column=0, sticky='w')
        
        # Cost labels with actual expenses and planned expenses
        self.total_cost = tk.Label(self.tab1, text="", font=("Arial", 16))
        self.total_cost.grid(row=10, column=1, sticky='e')
        self.total_planned_cost = tk.Label(self.tab1, text="", font=("Arial", 16))
        self.total_planned_cost.grid(row=10, column=2, sticky='e')
        
         # create a separator
        separator = ttk.Separator(self.tab1, orient='horizontal')
        separator.grid(row=11, column=0, columnspan=3, sticky='ew', pady=10)
        
        # Difference cost
        self.difference = tk.Label(self.tab1, text="", font=("Arial", 16))
        self.difference.grid(row=12, column=2, sticky='e')
        
        # Add expense button
        self.add_expense_button = tk.Button(self.tab1, text="Add expense", command=self.add_expense_window)
        self.add_expense_button.grid(row=13, column=0, columnspan=3, sticky='ew')
        
        self.import_button = tk.Button(self.tab1, text="Import..", command=self.import_expenses_window)
        self.import_button.grid(row=14, column=0, columnspan=3, sticky='ew')
        
        # Dropdown menu
        self.dropdown_countries = [country.title() for country in self.countries]
        if self.dropdown_countries == []:
            self.dropdown_countries = ["-"]
        self.country_name = tk.StringVar()
        self.country_name.trace_add('write', self.update_expenses)
        self.country_name.set(self.dropdown_countries[0])
        self.dropdown = tk.OptionMenu(self.tab1, self.country_name, *self.dropdown_countries)
        self.dropdown.grid(row=0, column=0, sticky='w', pady=10)
        self.dropdown.config(width=8)
        
        ### Tab 2 ###
        self.fixed_cost_label = tk.Label(self.tab2, text="Fixed costs")
        self.fixed_cost_label.grid(row=0, column=0, sticky='w')
        
        self.fixed_cost = tk.Label(self.tab2, text="0")
        self.fixed_cost.grid(row=0, column=1, sticky='e')
        
        self.add_fixed_cost_button = tk.Button(self.tab2, text="Add fixed cost", command=self.add_fixed_cost_window)
        self.add_fixed_cost_button.grid(row=1, column=0, columnspan=2, sticky='ew')

        self.update_expenses()
        
        self.window.mainloop()
        
    def add_country_window(self):
        add_country_window = tk.Toplevel(self.window)
        add_country_window.title("Add country")
        add_country_window.geometry("300x300")
        add_country_window.resizable(False, False)
        
        add_country_window.columnconfigure(0, weight=1)
        add_country_window.columnconfigure(1, weight=1)
        
        # Label
        tk.Label(add_country_window, text="Country:").grid(row=0, column=0, sticky="e")
        
        # Dropdown
        country_name = tk.StringVar()
        country_name.set(self.all_countries[0])
        country_dropdown = tk.OptionMenu(add_country_window, country_name, *self.all_countries)
        country_dropdown.grid(row=0, column=1, sticky="w")
        
        
    def add_fixed_cost_window(self):
        add_fixed_cost_window = tk.Toplevel(self.window)
        add_fixed_cost_window.title("Add fixed expense")
        add_fixed_cost_window.geometry("300x250")
        add_fixed_cost_window.resizable(False, False)
        
        add_fixed_cost_window.columnconfigure(0, weight=1)
        add_fixed_cost_window.columnconfigure(1, weight=1)
        
        # Create the labels for the input fields
        # def add_expense(self, name: str, cost: float, frequency="yearly", start_date=datetime.now(), end_date=datetime.now()):
        name_label = tk.Label(add_fixed_cost_window, text="Name")
        amount_label = tk.Label(add_fixed_cost_window, text="Amount")
        frequency_label = tk.Label(add_fixed_cost_window, text="Frequency")
        start_date_label = tk.Label(add_fixed_cost_window, text="Start Date")
        end_date_label = tk.Label(add_fixed_cost_window, text="End Date")
        
        # Create the entry fields and dropdown for each label
        name_entry = tk.Entry(add_fixed_cost_window, takefocus=True)
        frequency_name = tk.StringVar()
        frequency_name.set("Yearly")
        frequency_dropdown = tk.OptionMenu(add_fixed_cost_window, frequency_name, *["Yearly", "Monthly", "Weekly"])
        frequency_dropdown.config(width=16)
        amount_entry = tk.Entry(add_fixed_cost_window)
        date_entry = tk.Entry(add_fixed_cost_window, text=dt.datetime.now().strftime("%d.%m.%Y"))
        checkbox_var = tk.BooleanVar()
        is_planned_checkbox = tk.Checkbutton(add_fixed_cost_window, variable=checkbox_var)
        add_button = tk.Button(add_fixed_cost_window, text="Add", command=lambda: self.add_expense(name=name_entry.get(), category=frequency_name.get(), cost=amount_entry.get(), date=date_entry.get(), is_planned=checkbox_var.get()), state="disabled")
        
        # Add the widgets to the window using the grid layout
        name_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        name_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        frequency_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')
        frequency_dropdown.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        amount_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')
        amount_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        start_date_label.grid(row=3, column=0, padx=5, pady=5, sticky='w')
        date_entry.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        add_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky='ew')
        
    
    def add_expense_window(self):
        add_expense_window = tk.Toplevel(self.window)
        add_expense_window.title("Add expense")
        add_expense_window.geometry("300x260")
        add_expense_window.resizable(False, False)
        
        add_expense_window.columnconfigure(0, weight=1)
        add_expense_window.columnconfigure(1, weight=1)
            
        # Create the labels for the input fields
        name_label = tk.Label(add_expense_window, text="Name")
        category_label = tk.Label(add_expense_window, text="Category")
        amount_label = tk.Label(add_expense_window, text="Amount")
        date_label = tk.Label(add_expense_window, text="Date")
        is_planned_label = tk.Label(add_expense_window, text="Planned")
        country_label = tk.Label(add_expense_window, text="Country")
        
        # Create the entry fields and dropdown for each label
        name_entry = tk.Entry(add_expense_window, takefocus=True)
        category_name = tk.StringVar()
        category_name.set(self.categories[0].title())
        category_dropdown = tk.OptionMenu(add_expense_window, category_name, *[category.title() for category in self.categories])
        category_dropdown.config(width=16)
        amount_entry = tk.Entry(add_expense_window)
        date_entry = tk.Entry(add_expense_window, text=dt.datetime.now().strftime("%d.%m.%Y"))
        checkbox_var = tk.BooleanVar()
        is_planned_checkbox = tk.Checkbutton(add_expense_window, variable=checkbox_var)
        country_names = self.databases["country"].get_selected_countries()
        if len(country_names) <= 0:
            country_names = self.all_countries
        country_name = tk.StringVar()
        country_name.set(country_names[0])
        country_dropdown = tk.OptionMenu(add_expense_window, country_name, *country_names)
        add_button = tk.Button(add_expense_window, text="Add", command=lambda: self.add_expense(name=name_entry.get(), country=country_name.get(), category=category_name.get(), cost=amount_entry.get(), date=date_entry.get(), is_planned=checkbox_var.get()))
        
        # Add the widgets to the window using the grid layout
        name_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        name_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        country_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        country_dropdown.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        category_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')
        category_dropdown.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
        amount_label.grid(row=3, column=0, padx=5, pady=5, sticky='w')
        amount_entry.grid(row=3, column=1, padx=5, pady=5, sticky='ew')
        date_label.grid(row=4, column=0, padx=5, pady=5, sticky='w')
        date_entry.grid(row=4, column=1, padx=5, pady=5, sticky='ew')
        is_planned_label.grid(row=5, column=0, padx=5, pady=5, sticky='w')
        is_planned_checkbox.grid(row=5, column=1, padx=5, pady=5, sticky='ew')
        add_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky='ew')
        
    def import_expenses_window(self):
        import_expenses_window = tk.Toplevel(self.window)
        import_expenses_window.title("Import expenses")
        import_expenses_window.geometry("300x250")
        import_expenses_window.resizable(False, False)
        
        path_entry_label = tk.Label(import_expenses_window, text="Path to file")
        path_entry_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        path_entry = tk.Entry(import_expenses_window)
        path_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        path_entry.insert(0, "/Users/jonathankeller/Documents/Programming/finance-overview/data.csv")
        
        import_button = tk.Button(import_expenses_window, text="Import..", command=lambda: importer.mass_import(path=path_entry.get()))
        import_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

    def add_expense(self, name: str, country: str, category: str, cost: str, date: str, is_planned: bool):
        # Add the expense to the database
        added_successfully = self.databases["country"].add_expense(name=name, category=category, cost=cost, date=date, is_planned=is_planned, country=country)
        if not added_successfully:
            messagebox.showerror("Error", "There is something wrong with the input.")
            return
        else:
            messagebox.showinfo("Success", "Expense added successfully.")
        self.update_expenses()
        self.dropdown_countries = [country.title() for country in self.databases["country"].get_selected_countries()]
        self.country_name.set(self.dropdown_countries[0])
        self.dropdown['menu'].delete(0, 'end')
        for country in self.dropdown_countries:
            self.dropdown['menu'].add_command(label=country, command=tk._setit(self.country_name, country))
        
        
    
    def update_expenses(self, *args):
        # Update overview costs
        selected_country = self.country_name.get()
        total_cost_actual = self.databases["country"].get_total_cost(selected_country)
        total_cost_planned = self.databases["country"].get_total_cost(selected_country, is_planned=True)
        difference = total_cost_planned - total_cost_actual
        
        self.total_cost.config(text=f"{total_cost_actual:.2f} €")
        self.total_planned_cost.config(text=f"{total_cost_planned:.2f} €")
        self.difference.config(text=f"{difference:.2f} €", fg="red" if difference < 0 else "green")
        
        
        # Remove existing category labels
        for label in self.category_labels.values():
            label.destroy()
        
        self.category_labels = {}
        
        categories_actual = self.databases["country"].get_category_cost(selected_country)
        categories_planned = self.databases["country"].get_category_cost(selected_country, is_planned=True)
        
        for i, category in enumerate(self.categories):
            # Category Label
            label = tk.Label(self.tab1, text=category.capitalize())
            label.grid(row=i+3, column=0, sticky='w')
            self.category_labels[category] = label
            
            # Actual cost label
            try:
                actual_label = tk.Label(self.tab1, text=f"{categories_actual[category]:.2f} €")
            except KeyError:
                actual_label = tk.Label(self.tab1, text="0.00 €")
            
            actual_label.grid(row=i+3, column=1, sticky='e')
            self.category_labels[f"{category}_actual"] = actual_label
            
            # Planned cost label
            try:
                planned_label = tk.Label(self.tab1, text=f"{categories_planned[category]:.2f} €")
            except KeyError:
                planned_label = tk.Label(self.tab1, text="0.00 €")
            planned_label.grid(row=i+3, column=2, sticky='e')
            self.category_labels[f"{category}_planned"] = planned_label
            