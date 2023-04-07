from database import CountryDatabase, FixedDatabase, IncomeDatabase
from ui import UI
import ui

CATEGORIES = [
    "flights",
    "accommodation",
    "trips",
    "food",
    "transport",
    "other"
]

databases = {
    "country": CountryDatabase(),
    "fixed": FixedDatabase(),
    "income": IncomeDatabase()
}

# TODO Add Category Button in add expense window
# TODO Add Category method in UI class
# TODO Add fixed cost tab in add expense window
# TODO Add fixed cost button in fixed cost tab
# TODO Add button to set budget
# TODO Add button for income
# TODO Add income to budget
# TODO Save budget
# TODO compare daily expense vs budget plus income
    
if __name__ == "__main__":
    main_ui = UI(CATEGORIES, databases)
    