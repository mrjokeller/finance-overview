import tkinter as tk
from tkinter import ttk

from sqlalchemy import func


class UI:
    
    def __init__(self, countries: list, databases):
        self.databases = databases
        self.category_labels = {}
        self.window = tk.Tk()
        self.window.title("Finanzen")
        self.window.geometry("800x600")
        
        self.window.config(padx=20, pady=20)
        
        # Dropdown menu
        countries = [country.capitalize() for country in countries]
        self.country_name = tk.StringVar()
        self.country_name.trace_add('write', self.update_expenses)
        self.country_name.set(countries[0])
        self.dropdown = tk.OptionMenu(self.window, self.country_name, *countries)
        self.dropdown.grid(row=0, column=0, sticky='w', pady=20)
        self.dropdown.config(width=8)
        
        
        # Labels with total cost, total planned cost and total difference
        self.total_cost_label = tk.Label(self.window, text="Total cost: ", pady=20)
        self.total_cost_label.grid(row=1, column=0, sticky='w')
        self.total_planned_cost_label = tk.Label(self.window, text="Total planned cost: ")
        self.total_planned_cost_label.grid(row=2, column=0, sticky='w')
        self.total_difference_label = tk.Label(self.window, text="Total difference: ")
        self.total_difference_label.grid(row=1, column=2, sticky='w')
        
        # create a separator
        separator = ttk.Separator(self.window, orient='horizontal')
        separator.grid(row=3, column=0, columnspan=3, sticky='ew', pady=20)

        self.update_expenses()
        
        self.window.mainloop()
        
    
    def update_expenses(self, *args):
        selected_country = self.country_name.get().lower()
        
        total_cost_planned = self.databases[selected_country].get_total_cost(is_planned=True)
        self.total_planned_cost_label.config(text=f"Total planned cost: {total_cost_planned} €")
        total_cost_actual = self.databases[selected_country].get_total_cost()
        self.total_cost_label.config(text=f"Total cost: {total_cost_actual} €")
        difference = total_cost_planned - total_cost_actual
        if difference < 0:
            self.total_difference_label.config(text=f"Difference: {difference} €", fg="red")
        else:
            self.total_difference_label.config(text=f"Difference: {difference} €", fg="green")
        
        
        # Remove existing category labels
        for label in self.category_labels.values():
            label.destroy()
            
        self.categories = self.databases[selected_country].get_category_cost()
        if self.categories is None:
            return
        
        
        
        self.category_labels = {}
        for i, category in enumerate(self.categories):
            label = tk.Label(self.window, text=category.capitalize())
            label.grid(row=i+4, column=0, sticky='w')
            self.category_labels[category] = label
            
            value_label = tk.Label(self.window, text=self.categories[category])
            value_label.grid(row=i+4, column=1, sticky='e')
            self.category_labels[f"{category}_value"] = value_label
        
        

