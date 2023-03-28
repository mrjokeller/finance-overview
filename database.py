from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class CountryExpense(Base):
    __tablename__ = 'country_expenses'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    cost = Column(Integer)
    category = Column(String)
    is_planned = Column(Boolean)

    def __repr__(self):
        return f"<CountryExpense(name='{self.name}', cost='{self.cost}', category='{self.category}', is_planned='{self.is_planned}')>"

class CountryDatabase:
    def __init__(self, db_name):
        self.engine = create_engine(f'sqlite:///{db_name}.db')
        # Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_expense(self, name, cost, category, is_planned=True):
        session = self.Session()
        expense = CountryExpense(name=name, cost=cost, category=category, is_planned=is_planned)
        session.add(expense)
        session.commit()
        session.close()

    def get_all_expenses(self):
        session = self.Session()
        expenses = session.query(CountryExpense).all()
        session.close()
        return expenses
