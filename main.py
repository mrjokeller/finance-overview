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
# databases["southafrica"].add_expense(name="test", cost=100, category="food", is_planned=True)





def main():
    pass
    # ui = UI()
    
    
if __name__ == "__main__":
    main()
    