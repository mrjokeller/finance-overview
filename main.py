from sqlalchemy import Column, Float, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from database import CountryDatabase

from ui import UI

COUNTRIES = [
    "southafrica",
    "mauritius",
    "kenya",
    "tanzania",
    "israel",
    "egypt",
    "morocco",
    "uae",
    "thailand",
    "vietnam",
    "malaysia",
    "indonesia",
    "india",
    "nepal",
    "philippines",
    "japan",
    "mexico",
    "cuba",
    "europe",
    "costarica",
    "panama",
    "argentina",
    "chile",
    "brazil",
    "peru",
    "hawaii",
    "indonesia",
    "australia",
    "newzealand"
]

databases = {country: CountryDatabase(country) for country in COUNTRIES}


def main():
    db = databases["southafrica"]
    # db.add_expense("test", 10.0)
    total_cost = db.get_total_cost(categories=["food"])
    
    print(f"{total_cost:.2f} EUR")
    # ui = UI()
    
    
if __name__ == "__main__":
    main()
    