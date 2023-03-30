from operator import and_
from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime, create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()


class CountryExpense(Base):
    __tablename__ = 'country_expenses'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    cost = Column(Float)
    category = Column(String)
    is_planned = Column(Boolean)
    date = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<CountryExpense(name='{self.name}', cost='{self.cost}', category='{self.category}', is_planned='{self.is_planned}', date='{self.date}')>"
    
class FixedCost(Base):
    __tablename__ = 'fixed_costs'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    cost = Column(Float)
    frequency = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    
    def __repr__(self):
        return f"<FixedCost(name='{self.name}', cost='{self.cost}', frequency='{self.frequency}', start_date='{self.start_date}', end_date='{self.end_date}')>"

class CountryDatabase:
    def __init__(self, db_name):
        self.country_engine = create_engine(f'sqlite:///databases/{db_name}.db')
        self.fixed_engine = create_engine('sqlite:///databases/fixed.db')
        # Only activate the following line to create the database
        Base.metadata.create_all(self.country_engine)
        Base.metadata.create_all(self.fixed_engine)
        self.Session = sessionmaker(bind=self.country_engine)

    def add_expense(self, name: str, cost: float, category="other", is_planned=False, date=datetime.now()):
        session = self.Session()
        expense = CountryExpense(name=name, cost=cost, category=category, is_planned=is_planned, date=date)
        session.add(expense)
        session.commit()
        session.close()
        
    def edit_expense(self, expense_id: int, new_cost: float, new_category: str, is_planned: bool, date: datetime):
        session = self.Session()

        # query for expense by country name and expense id
        expense = session.query(CountryExpense).filter_by(id=expense_id).first()

        # update expense attributes
        expense.cost = new_cost
        expense.category = new_category
        expense.is_planned = is_planned
        expense.date = date

        # commit changes and close session
        session.commit()
        session.close()
        
    def delete_country_expense(self, entry_id):
        session = self.Session()
        entry_to_delete = session.query(CountryExpense).filter_by(id=entry_id).first()
        if entry_to_delete:
            session.delete(entry_to_delete)
            session.commit()
            print(f"Country expense with id {entry_id} deleted successfully.")
        else:
            print(f"No country expense found with id {entry_id}.")

    def get_all_expenses(self):
        session = self.Session()
        expenses = session.query(CountryExpense).all()
        session.close()
        return expenses
    
    def get_total_cost(self, categories=None, is_planned=False):
        """Returns the total cost of all expenses in the database.

        Args:
            categories (list, optional): Specify categories. Defaults to None.
            is_planned (bool, optional): Specify if the expenses are planned or not. Input None for planned and unplanned expenses. Defaults to False.

        Returns:
            float: Total cost of all expenses in the database.
        """
        session = self.Session()
        query = session.query(func.sum(CountryExpense.cost))
        if categories:
            query = query.filter(CountryExpense.category.in_(categories))
        if is_planned is not None:
            query = query.filter(CountryExpense.is_planned == is_planned)
        if categories and is_planned is not None:
            query = query.filter(and_(CountryExpense.category.in_(categories), CountryExpense.is_planned == is_planned))
        total_cost = query.scalar()
        return total_cost or 0

    def get_category_cost(self, is_planned=False):
        """Returns the total cost of all expenses in the database.

        Args:
            category (str): Specify category.
            is_planned (bool, optional): Specify if the expenses are planned or not. Input None for planned and unplanned expenses. Defaults to False.

        Returns:
            dict: Total cost of all expenses in the database per category.
        """
        session = self.Session()
        categories = session.query(CountryExpense.category, func.sum(CountryExpense.cost)).\
                                                                filter(CountryExpense.is_planned == is_planned).\
                                                                group_by(CountryExpense.category).\
                                                                order_by(CountryExpense.category).\
                                                                all()
        categories_dict = {category: cost for category, cost in categories}
        return categories_dict or {}