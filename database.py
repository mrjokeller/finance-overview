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
        # Only activate the following line to create the database
        # Base.metadata.create_all(self.country_engine, tables=[CountryExpense.__table__])
        self.CountrySession = sessionmaker(bind=self.country_engine)

        
    def add_expense(self, name: str, cost: str, category: str, is_planned: bool, date: str):
        session = self.CountrySession()
        # Convert all values to the correct type
        if name == "":
            return False
        try:
            name = str(name).capitalize()
        except Exception as e:
            print(e)
            return False

        try:
            category = str(category).lower()
        except Exception as e:
            print(e)
            return False

        try:
            cost = float(cost.replace(",", ".")) if cost else 0
        except Exception as e:
            print(e)
            return False

        try:
            if date:
                date = date.split(".")
                date = datetime(year=int(date[2]), month=int(date[1]), day=int(date[0]))
            else:
                date = datetime.now()
        except Exception as e:
            print(e)
            return False
        
        else:
            expense = CountryExpense(name=name, cost=cost, category=category, is_planned=is_planned, date=date)
            session.add(expense)
            session.commit()
            session.close()
            return True
        
    def edit_expense(self, expense_id: int, new_cost: float, new_category: str, is_planned: bool, date: datetime):
        session = self.CountrySession()

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
        
    def delete_expense(self, entry_id):
        session = self.CountrySession()
        entry_to_delete = session.query(CountryExpense).filter_by(id=entry_id).first()
        if entry_to_delete:
            session.delete(entry_to_delete)
            session.commit()
            print(f"Country expense with id {entry_id} deleted successfully.")
        else:
            print(f"No country expense found with id {entry_id}.")

    def get_all_expenses(self):
        session = self.CountrySession()
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
        session = self.CountrySession()
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
        session = self.CountrySession()
        categories = session.query(CountryExpense.category, func.sum(CountryExpense.cost)).\
                                                                filter(CountryExpense.is_planned == is_planned).\
                                                                group_by(CountryExpense.category).\
                                                                order_by(CountryExpense.category).\
                                                                all()
        categories_dict = {category: cost for category, cost in categories}
        return categories_dict or {}
    
class FixedDatabase:
    
    def __init__(self):
        self.fixed_engine = create_engine('sqlite:///databases/fixed_costs.db')
        # Only activate the following line to create the database
        # Base.metadata.create_all(self.fixed_engine, tables=[FixedCost.__table__])
        self.FixedSession = sessionmaker(bind=self.fixed_engine)

    def add_expense(self, name: str, cost: float, frequency="yearly", start_date=datetime.now(), end_date=datetime.now()):
        session = self.FixedSession()
        expense = FixedCost(name=name, cost=cost, frequency=frequency, start_date=start_date, end_date=end_date)
        session.add(expense)
        session.commit()
        session.close()
        
    def edit_expense(self, expense_id: int, new_cost: float, new_frequency: str, new_start_date: datetime, new_end_date: datetime):
        session = self.FixedSession()

        # query for expense by country name and expense id
        expense = session.query(FixedCost).filter_by(id=expense_id).first()

        # update expense attributes
        expense.cost = new_cost
        expense.frequency = new_frequency
        expense.start_date = new_start_date
        expense.end_date = new_end_date

        # commit changes and close session
        session.commit()
        session.close()
        
    def delete_expense(self, entry_id):
        session = self.FixedSession()
        entry_to_delete = session.query(FixedCost).filter_by(id=entry_id).first()
        if entry_to_delete:
            session.delete(entry_to_delete)
            session.commit()
            print(f"Fixed expense with id {entry_id} deleted successfully.")
        else:
            print(f"No fixed expense found with id {entry_id}.")

    def get_all_expenses(self):
        session = self.FixedSession()
        expenses = session.query(FixedCost).all()
        session.close()
        return expenses
    
    def get_total_cost(self):
        """Returns the total cost of all fixed expenses in the database.

        Returns:
            float: Total cost of all fixed expenses in the database.
        """
        
        session = self.FixedSession()
        query = session.query(func.sum(FixedCost.cost))
        total_cost = query.scalar()
        return total_cost or 0
