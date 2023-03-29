import tkinter as tk
from tkinter import ttk


class UI:
    
    def __init__(self, countries: list, categories: list, databases):
        self.databases = databases
        self.categories = categories
        self.category_labels = {}
        self.window = tk.Tk()
        self.window.title("Finanzen")
        self.window.geometry("500x500")
        
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
        
        self.subheading_label = tk.Label(self.window, text="Categories", font=("Arial", 16))
        self.subheading_label.grid(row=4, column=0, sticky='w')
        self.subheading_label_2 = tk.Label(self.window, text="Actual", font=("Arial", 16))
        self.subheading_label_2.grid(row=4, column=1, sticky='w')
        self.subheading_label_3 = tk.Label(self.window, text="Planned", font=("Arial", 16))
        self.subheading_label_3.grid(row=4, column=2, sticky='e')

        self.update_expenses()
        
        self.window.mainloop()
        
    
    def update_expenses(self, *args):
        selected_country = self.country_name.get().lower()
        
        # Update total cost labels
        total_cost_actual = self.databases[selected_country].get_total_cost()
        total_cost_planned = self.databases[selected_country].get_total_cost(is_planned=True)
        difference = total_cost_planned - total_cost_actual
        
        self.total_cost_label.config(text=f"Total cost: {total_cost_actual:.2f} €")
        self.total_planned_cost_label.config(text=f"Total planned cost: {total_cost_planned:.2f} €")
        self.total_difference_label.config(text=f"Difference: {difference:.2f} €", fg="red" if difference < 0 else "green")
        
        
        # Remove existing category labels
        for label in self.category_labels.values():
            label.destroy()
        
        self.category_labels = {}
        
        categories_actual = self.databases[selected_country].get_category_cost()
        categories_planned = self.databases[selected_country].get_category_cost(is_planned=True)
        
        for i, category in enumerate(self.categories):
            # Category Label
            label = tk.Label(self.window, text=category.capitalize())
            label.grid(row=i+5, column=0, sticky='w')
            self.category_labels[category] = label
            
            # Actual cost label
            try:
                actual_label = tk.Label(self.window, text=categories_actual[category])
            except KeyError:
                actual_label = tk.Label(self.window, text="0.00")
            
            actual_label.grid(row=i+5, column=1, sticky='e')
            self.category_labels[f"{category}_actual"] = actual_label
            
            # Planned cost label
            try:
                planned_label = tk.Label(self.window, text=categories_planned[category])
            except KeyError:
                planned_label = tk.Label(self.window, text="0.00")
            planned_label.grid(row=i+5, column=2, sticky='e')
            self.category_labels[f"{category}_planned"] = planned_label

