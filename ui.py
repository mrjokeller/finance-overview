import tkinter as tk


class UI:
    
    def __init__(self, countries: list, databases):
        self.databases = databases
        self.window = tk.Tk()
        self.window.title("Finanzen")
        self.window.geometry("800x600")
        
        self.window.config(padx=20, pady=20)
        
        # Dropdown menu
        countries = [country.capitalize() for country in countries]
        self.country_name = tk.StringVar()
        self.country_name.set(countries[0])
        self.dropdown = tk.OptionMenu(self.window, self.country_name, *countries)
        self.dropdown.grid(row=0, column=0)
        self.dropdown.config(width=8)
        
        # Labels with total cost, total planned cost and total difference
        self.total_cost_label = tk.Label(self.window, text="Total cost: ", pady=20)
        self.total_cost_label.grid(row=1, column=0)
        self.total_planned_cost_label = tk.Label(self.window, text="Total planned cost: ")
        self.total_planned_cost_label.grid(row=2, column=0)
        self.total_difference_label = tk.Label(self.window, text="Total difference: ")
        self.total_difference_label.grid(row=1, column=1)
        
        self.show_expenses()
        
        self.window.mainloop()
        
    def show_expenses(self):
        total_cost_planned = self.databases[self.country_name.get().lower()].get_total_cost(is_planned=True)
        self.total_planned_cost_label.config(text=f"Total planned cost: {total_cost_planned} €")
        total_cost_actual = self.databases[self.country_name.get().lower()].get_total_cost()
        self.total_cost_label.config(text=f"Total cost: {total_cost_actual} €")
        self.total_difference_label.config(text=f"Total difference: {total_cost_actual - total_cost_planned} €")