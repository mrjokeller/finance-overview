from ui import UI
from sqlalchemy import Column, Float, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base


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

engines = [create_engine(f"sqlite:///{country}.db") for country in COUNTRIES]
Base = declarative_base()

class CountryExpense(Base):
    __tablename__ = 'country_expense'
    id = Column(Integer, primary_key=True)
    country = Column(String)
    flight = Column(Float)
    accommodation = Column(Float)
    trips = Column(Float)
    food = Column(Float)
    transport = Column(Float)
    other = Column(Float)





def main():
    ui = UI()
    
    
if __name__ == "__main__":
    main()
    