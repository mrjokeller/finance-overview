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

# TODO Add fixed cost button in fixed cost tab
# TODO Update fixed database methods
# TODO update mass import
# TODO Add button to set budget
# TODO Add button for income
# TODO Add income to budget
# TODO Save budget
# TODO compare daily expense vs budget plus income
# TODO new tab with overview (like country overview)
    
if __name__ == "__main__":
    main_ui = UI(CATEGORIES, databases)
    