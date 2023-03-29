from database import CountryDatabase
from ui import UI

COUNTRIES = [
    "south africa",
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
    "new zealand"
]
CATEGORIES = [
    "flights",
    "accommodation",
    "trips",
    "food",
    "transport",
    "other"
]

databases = {country: CountryDatabase(country.replace(" ", "")) for country in COUNTRIES}


def main():
    ui = UI(COUNTRIES, CATEGORIES, databases)
    
    
if __name__ == "__main__":
    main()
    