from database import CountryDatabase, FixedDatabase, IncomeDatabase
from ui import UI

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
    
    
if __name__ == "__main__":
    ui = UI(CATEGORIES, databases)
    