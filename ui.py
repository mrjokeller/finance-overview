import datetime as dt
import tkinter as tk
from tkinter import ttk, messagebox
import importer
import json


def get_countries():
    with open("./data.json", "r") as f:
        countries_dict = json.load(f)
    return countries_dict["countries"]

def add_country(country: str):
    countries = get_countries()
    countries["countries"].extend(country.lower())
    countries["countries"].sort()
    with open("./data.json", "w") as f:
        json.dumps(countries)
        
def get_categories() -> dict:
    """
    Read the 'categories' object from a JSON file and return it as a dictionary.

    Returns:
        A dictionary containing the 'categories' object from the JSON file.

    Raises:
        FileNotFoundError: If the file './data.json' cannot be found.
        json.JSONDecodeError: If the JSON file is invalid and cannot be decoded.

    """
    with open("./data.json", "r") as f:
        categories_dict = json.load(f)["categories"]
    return categories_dict
    
def add_category(sub_category: str, main_category="other"):
    for list in get_categories().values():
        if sub_category.lower() in list:
            messagebox.showwarning(title="Warning", message=f"The category '{sub_category.capitalize()}' already exists.")
            return
    if messagebox.askokcancel(title="Check again", message=f"Is this right?\nCategory: {sub_category}\nMain Category: {main_category}"):
        with open("./data.json", "r") as f:
            data = json.load(f)
        with open("./data.json", "w") as f:
            data["categories"][main_category.lower()].append(sub_category.lower())
            json.dump(data, f, indent=4)
            messagebox.showinfo(title="Success", message=f"New category '{sub_category}' successfully saved.")
        

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
        self.categories = get_categories()
        self.all_countries = get_countries()
        self.countries = databases["country"].get_selected_countries()
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
        
        # Dropdown menu
        self.dropdown_countries = [country.title() for country in self.countries]
        if self.dropdown_countries == []:
            self.dropdown_countries = ["-"]
        self.country_name = tk.StringVar()
        self.country_name.set(self.dropdown_countries[0])
        self.country_name.trace_add('write', self.update_expenses)
        self.dropdown = tk.OptionMenu(self.tab1, self.country_name, *self.dropdown_countries)
        self.dropdown.grid(row=0, column=0, sticky='w', pady=10)
        self.dropdown.config(width=8)
        
        # Add expense button
        self.add_expense_button = tk.Button(self.tab1, text="Add expense", command=self.add_expense_window)
        self.add_expense_button.grid(row=13, column=0, columnspan=3, sticky='ew')
        
        self.import_button = tk.Button(self.tab1, text="Import..", command=self.import_expenses_window)
        self.import_button.grid(row=14, column=0, columnspan=3, sticky='ew')
        
        ### Tab 2 ###
        self.fixed_cost_label = tk.Label(self.tab2, text="Fixed costs")
        self.fixed_cost_label.grid(row=0, column=0, sticky='w')
        
        self.fixed_cost = tk.Label(self.tab2, text="0")
        self.fixed_cost.grid(row=0, column=1, sticky='e')
        
        self.add_fixed_cost_button = tk.Button(self.tab2, text="Add fixed cost", command=self.add_fixed_cost_window)
        self.add_fixed_cost_button.grid(row=1, column=0, columnspan=2, sticky='ew')

        self.update_expenses()
        
        self.window.mainloop()
          
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
        add_expense_window.geometry("400x380")
        add_expense_window.resizable(False, False)
        add_expense_window.config(padx=10, pady=10)
        
        # add_expense_window.columnconfigure(0, weight=1)
        # add_expense_window.columnconfigure(1, weight=1)
        
        # Setup tabs
        tabview = ttk.Notebook(add_expense_window, width=330, height=280)
        tab1 = ttk.Frame(tabview)
        tab2 = ttk.Frame(tabview)
        tabview.add(tab1, text="Standard")
        tabview.add(tab2, text="Fixed")
        tabview.grid(row=0, column=0, columnspan=3, sticky='nsew')
        
        tab1.columnconfigure(0, weight=1)
        tab1.columnconfigure(1, weight=1)
        tab1.columnconfigure(2, weight=1)
        tab2.columnconfigure(0, weight=1)
        tab2.columnconfigure(1, weight=1)
        tab2.columnconfigure(2, weight=1)
        
        ### Tab 1 - Standard expense entry ###
        # Create the labels for the input fields
        name_label = tk.Label(tab1, text="Name")
        country_label = tk.Label(tab1, text="Country")
        category_label = tk.Label(tab1, text="Category")
        amount_label = tk.Label(tab1, text="Amount")
        date_label = tk.Label(tab1, text="Date")
        is_planned_label = tk.Label(tab1, text="Planned")
        
        # Create the entry fields and dropdown for each label
        name_entry = tk.Entry(tab1, takefocus=True)
        # Category Dropdown
        categories = [subcategory.title() for category in self.categories.values() for subcategory in category]
        category_name = tk.StringVar()
        category_name.set(categories[0])
        category_dropdown = tk.OptionMenu(
            tab1, 
            category_name, 
            *categories)
        category_dropdown.config(width=16)
        # Entries
        amount_entry = tk.Entry(tab1)
        date_entry = tk.Entry(tab1)
        date_entry.insert(0, dt.datetime.now().strftime("%d.%m.%Y"))
        checkbox_var = tk.BooleanVar()
        is_planned_checkbox = tk.Checkbutton(tab1, variable=checkbox_var)
        # Country dropdown
        country_names = self.all_countries
        country_name = tk.StringVar()
        country_name.set(self.country_name.get())
        country_dropdown = tk.OptionMenu(
            tab1, 
            country_name, 
            *[country.title() for country in country_names])
        # Buttons
        add_button = tk.Button(
            tab1, 
            text="Add", 
            command=lambda: self.add_expense(name=name_entry.get(), country=country_name.get(), category=category_name.get(), cost=amount_entry.get(), date=date_entry.get(), is_planned=checkbox_var.get()))
        add_category_button = tk.Button(
            tab1,
            text="+",
            command=self.add_category_window
        )
        
        # Add the widgets to the window using the grid layout
        name_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        name_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky='ew')
        country_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        country_dropdown.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
        category_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')
        category_dropdown.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
        add_category_button.grid(row=2, column=2, padx=5, pady=5, sticky='ew')
        amount_label.grid(row=3, column=0, padx=5, pady=5, sticky='w')
        amount_entry.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky='ew')
        date_label.grid(row=4, column=0, padx=5, pady=5, sticky='w')
        date_entry.grid(row=4, column=1, columnspan=2, padx=5, pady=5, sticky='ew')
        is_planned_label.grid(row=5, column=0, padx=5, pady=5, sticky='w')
        is_planned_checkbox.grid(row=5, column=1, padx=5, pady=5, sticky='ew')
        add_button.grid(row=6, column=0, columnspan=3, padx=5, pady=5, sticky='ew')
        
        ### Tab 2 - Fixed cost entry ###
        name_label2 = tk.Label(tab2, text="Name")
        cost_label2 = tk.Label(tab2, text="Cost")
        frequency_label = tk.Label(tab2, text="Frequency")
        category_label2 = tk.Label(tab2, text="Category")
        start_date_label = tk.Label(tab2, text="Start Date")
        end_date_label = tk.Label(tab2, text="End Date")
        
        # Entries
        name_entry2 = tk.Entry(tab2)
        cost_entry = tk.Entry(tab2)
        start_date_entry = tk.Entry(tab2)
        end_date_entry = tk.Entry(tab2)
        
        # Dropdowns
        frequencies = ['Daily', 'Weekly', 'Biweekly', 'Monthly', 'Quarterly', 'Semi-Annually', 'Annually']
        frequency_var = tk.StringVar()
        frequency_var.set(frequencies[3])
        frequency_dropdown = tk.OptionMenu(tab2, frequency_var, *frequencies)
        
        category_name2 = tk.StringVar()
        category_name2.set(categories[0])
        category_dropdown2 = tk.OptionMenu(tab2, category_name2, *categories) # *categories is defined in tab1 for the category dropdown
        category_dropdown2.config(width=16)
        
        # Buttons
        add_button2 = tk.Button(
            tab2, 
            text="Add", 
            command=lambda: self.add_fixed_expense(name=name_entry.get(), country=country_name.get(), category=category_name.get(), cost=amount_entry.get(), date=date_entry.get(), is_planned=checkbox_var.get()))
        add_category_button2 = tk.Button(
            tab2,
            text="+",
            command=self.add_category_window
        )
        
        # Grid placement of all elements
        name_label2.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        name_entry2.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky='ew')
        cost_label2.grid(row=1, column=0, padx=5, pady=5, sticky='w')
        cost_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky='ew')
        frequency_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')
        frequency_dropdown.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky='ew')
        category_label2.grid(row=3, column=0, padx=5, pady=5, sticky='w')
        category_dropdown2.grid(row=3, column=1, padx=5, pady=5, sticky='ew')
        add_category_button2.grid(row=3, column=2, padx=5, pady=5, sticky='ew')
        start_date_label.grid(row=4, column=0, padx=5, pady=5, sticky='w')
        start_date_entry.grid(row=4, column=1, columnspan=2, padx=5, pady=5, sticky='ew')
        end_date_label.grid(row=5, column=0, padx=5, pady=5, sticky='w')
        end_date_entry.grid(row=5, column=1, columnspan=2, padx=5, pady=5, sticky='ew')
        add_button2.grid(row=6, column=0, columnspan=3, padx=5, pady=5, sticky='ew')
        
        
    def add_category_window(self):
        add_category_window = tk.Toplevel(self.window)
        add_category_window.title("Add category")
        add_category_window.config(padx=20, pady=20)
        add_category_window.resizable(False, False)
        
        tk.Label(add_category_window, text="Category").grid(row=0, column=0, sticky="w")
        tk.Label(add_category_window, text="Main Category").grid(row=1, column=0, sticky="w")
        
        category_entry = tk.Entry(add_category_window)
        main_category_var = tk.StringVar()
        main_category_var.set("Other")
        main_categories = ["Flights", "Accommodation", "Trips", "Food", "Transport", "Other"]
        main_category_dropdown = tk.OptionMenu(add_category_window, main_category_var, *main_categories)
        add_button = tk.Button(add_category_window, text="Add", command=lambda: add_category(sub_category=category_entry.get(), main_category=main_category_var.get()))
        
        category_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        main_category_dropdown.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        add_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        
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
            