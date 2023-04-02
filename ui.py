import datetime as dt
import tkinter as tk
from tkinter import ttk, messagebox
import importer


class UI:
    
    def __init__(self, countries: list, categories: list, databases):
        self.databases = databases
        self.categories = categories
        self.category_labels = {}
        self.window = tk.Tk()
        self.window.title("Finanzen")
        self.window.geometry("500x450")
        self.window.minsize(300, 400)
        
        self.window.config(padx=20, pady=20)
        
        self.window.grid_columnconfigure(0, weight=2, uniform="fred")
        self.window.grid_columnconfigure(1, weight=1, uniform="fred")
        self.window.grid_columnconfigure(2, weight=1, uniform="fred")
        
        # create a separator
        separator = ttk.Separator(self.window, orient='horizontal')
        separator.grid(row=1, column=0, columnspan=3, sticky='ew', pady=20)
        
        self.subheading_label = tk.Label(self.window, text="Categories", font=("Arial", 16))
        self.subheading_label.grid(row=2, column=0, sticky='w')
        self.subheading_label_2 = tk.Label(self.window, text="Actual", font=("Arial", 16))
        self.subheading_label_2.grid(row=2, column=1, sticky='e')
        self.subheading_label_3 = tk.Label(self.window, text="Planned", font=("Arial", 16))
        self.subheading_label_3.grid(row=2, column=2, sticky='e')
        
        # create a separator
        separator = ttk.Separator(self.window, orient='horizontal')
        separator.grid(row=9, column=0, columnspan=3, sticky='ew', pady=20)
        
        # Labels with total cost, total planned cost and total difference
        self.total_cost_label = tk.Label(self.window, text="Total:", font=("Arial", 16))
        self.total_cost_label.grid(row=10, column=0, sticky='w')
        self.total_difference_label = tk.Label(self.window, text="Difference: ", font=("Arial", 16))
        self.total_difference_label.grid(row=12, column=0, sticky='w')
        
        # Cost labels with actual expenses and planned expenses
        self.total_cost = tk.Label(self.window, text="", font=("Arial", 16))
        self.total_cost.grid(row=10, column=1, sticky='e')
        self.total_planned_cost = tk.Label(self.window, text="", font=("Arial", 16))
        self.total_planned_cost.grid(row=10, column=2, sticky='e')
        
         # create a separator
        separator = ttk.Separator(self.window, orient='horizontal')
        separator.grid(row=11, column=0, columnspan=3, sticky='ew', pady=20)
        
        # Difference cost
        self.difference = tk.Label(self.window, text="", font=("Arial", 16))
        self.difference.grid(row=12, column=2, sticky='e')
        
        # Add expense button
        self.add_expense_button = tk.Button(self.window, text="Add expense", command=self.add_expense_window)
        self.add_expense_button.grid(row=13, column=0, columnspan=3, sticky='ew')
        
        self.import_button = tk.Button(self.window, text="Import..", command=self.import_expenses_window)
        self.import_button.grid(row=14, column=0, columnspan=3, sticky='ew')
        
        # Dropdown menu
        countries = [country.title() for country in countries]
        self.country_name = tk.StringVar()
        self.country_name.trace_add('write', self.update_expenses)
        self.country_name.set(countries[0])
        self.dropdown = tk.OptionMenu(self.window, self.country_name, *countries)
        self.dropdown.grid(row=0, column=0, sticky='w', pady=10)
        self.dropdown.config(width=8)

        self.update_expenses()
        
        self.window.mainloop()
    
    def add_expense_window(self):
        add_expense_window = tk.Toplevel(self.window)
        add_expense_window.title("Add expense")
        add_expense_window.geometry("300x250")
        add_expense_window.resizable(False, False)
        
        add_expense_window.columnconfigure(0, weight=1)
        add_expense_window.columnconfigure(1, weight=1)
            
        # Create the labels for the input fields
        name_label = tk.Label(add_expense_window, text="Name")
        category_label = tk.Label(add_expense_window, text="Category")
        amount_label = tk.Label(add_expense_window, text="Amount")
        date_label = tk.Label(add_expense_window, text="Date")
        is_planned_label = tk.Label(add_expense_window, text="Planned")
        
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
        add_button = tk.Button(add_expense_window, text="Add", command=lambda: self.add_expense(name=name_entry.get(), category=category_name.get(), cost=amount_entry.get(), date=date_entry.get(), is_planned=checkbox_var.get()))
        
        # Add the widgets to the window using the grid layout
        name_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        name_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        category_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')
        category_dropdown.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        amount_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')
        amount_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        date_label.grid(row=3, column=0, padx=5, pady=5, sticky='w')
        date_entry.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        is_planned_label.grid(row=4, column=0, padx=5, pady=5, sticky='w')
        is_planned_checkbox.grid(row=4, column=1, padx=5, pady=5, sticky='w')
        add_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky='ew')
        
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
        
        selected_country = self.country_name.get().lower()
        import_button = tk.Button(import_expenses_window, text="Import..", command=lambda: importer.mass_import(path=path_entry.get()))
        import_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

    def add_expense(self, name: str, category: str, cost: str, date: str, is_planned: bool):
        # Add the expense to the database
        selected_country = self.country_name.get().lower()
        added_successfully = self.databases[selected_country].add_expense(name=name, category=category, cost=cost, date=date, is_planned=is_planned)
        if not added_successfully:
            messagebox.showerror("Error", "There is something wrong with the input.")
            return
        else:
            messagebox.showinfo("Success", "Expense added successfully.")
        self.update_expenses()
    
    def update_expenses(self, *args):
        selected_country = self.country_name.get().lower()
        # Update overview costs
        total_cost_actual = self.databases[selected_country].get_total_cost()
        total_cost_planned = self.databases[selected_country].get_total_cost(is_planned=True)
        difference = total_cost_planned - total_cost_actual
        
        self.total_cost.config(text=f"{total_cost_actual:.2f} €")
        self.total_planned_cost.config(text=f"{total_cost_planned:.2f} €")
        self.difference.config(text=f"{difference:.2f} €", fg="red" if difference < 0 else "green")
        
        
        # Remove existing category labels
        for label in self.category_labels.values():
            label.destroy()
        
        self.category_labels = {}
        
        categories_actual = self.databases[selected_country].get_category_cost()
        categories_planned = self.databases[selected_country].get_category_cost(is_planned=True)
        
        for i, category in enumerate(self.categories):
            # Category Label
            label = tk.Label(self.window, text=category.capitalize())
            label.grid(row=i+3, column=0, sticky='w')
            self.category_labels[category] = label
            
            # Actual cost label
            try:
                actual_label = tk.Label(self.window, text=f"{categories_actual[category]:.2f} €")
            except KeyError:
                actual_label = tk.Label(self.window, text="0.00 €")
            
            actual_label.grid(row=i+3, column=1, sticky='e')
            self.category_labels[f"{category}_actual"] = actual_label
            
            # Planned cost label
            try:
                planned_label = tk.Label(self.window, text=f"{categories_planned[category]:.2f} €")
            except KeyError:
                planned_label = tk.Label(self.window, text="0.00 €")
            planned_label.grid(row=i+3, column=2, sticky='e')
            self.category_labels[f"{category}_planned"] = planned_label
        