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
    ui = UI(COUNTRIES, databases)
    print(databases["southafrica"].get_category_cost())
    
    
if __name__ == "__main__":
    main()
    