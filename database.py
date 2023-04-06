from operator import and_
from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime, create_engine, distinct, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()


class Expense(Base):
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    cost = Column(Float)
    category = Column(String)
    is_planned = Column(Boolean)
    date = Column(DateTime, default=datetime.now)
    country = Column(String)

    def __repr__(self):
        return f"<Expense(name='{self.name}', cost='{self.cost}', category='{self.category}', is_planned='{self.is_planned}', date='{self.date}', country='{self.country}')>"
    
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
    
class Income(Base):
    __tablename__ = 'income'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    amount = Column(Float)
    category = Column(String)
    date = Column(DateTime)
    country = Column(String)
    
    def __repr__(self) -> str:
        return f"<Income(name='{self.name}', amount='{self.amount}', category='{self.category}', date='{self.date}', country='{self.country}')>"

class CountryDatabase:
    def __init__(self):
        self.engine = create_engine(f'sqlite:///expenses.db')
        # Only activate the following line to create the database
        # Base.metadata.create_all(self.country_engine)
        self.Session = sessionmaker(bind=self.engine)
        self.table_name = Expense

    def add_expense(self, name: str, cost: str, category: str, is_planned: bool, date: str, country: str):
        session = self.Session()
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
        
        try:
            country = country.lower()
        except Exception as e:
            print(e)
            return False
        
        else:
            expense = Expense(name=name, cost=cost, category=category, is_planned=is_planned, date=date, country=country)
            session.add(expense)
            session.commit()
            session.close()
            return True
        
    def edit_expense(self, expense_id: int, new_cost: float, new_country: str, new_category: str, is_planned: bool, date: datetime):
        session = self.Session()

        # query for expense by country name and expense id
        expense = session.query(Expense).filter_by(id=expense_id).first()

        # update expense attributes
        expense.cost = new_cost
        expense.country = new_country
        expense.category = new_category
        expense.is_planned = is_planned
        expense.date = date

        # commit changes and close session
        session.commit()
        session.close()
        
    def delete_expense(self, entry_id):
        session = self.Session()
        entry_to_delete = session.query(Expense).filter_by(id=entry_id).first()
        if entry_to_delete:
            session.delete(entry_to_delete)
            session.commit()
            print(f"Country expense with id {entry_id} deleted successfully.")
        else:
            print(f"No country expense found with id {entry_id}.")

    def get_all_expenses(self):
        session = self.Session()
        expenses = session.query(Expense).all()
        session.close()
        return expenses
    
    def get_total_cost(self, country: str, categories=None, is_planned=False):
        """Returns the total cost of all expenses in the database.

        Args:
            categories (list, optional): Specify categories. Defaults to None.
            is_planned (bool, optional): Specify if the expenses are planned or not. Input None for planned and unplanned expenses. Defaults to False.

        Returns:
            float: Total cost of all expenses in the database.
        """
        session = self.Session()
        query = session.query(func.sum(Expense.cost)).filter(Expense.country == country.lower())
        query.scalar()
        if categories:
            query = query.filter(Expense.category.in_(categories))
        if is_planned is not None:
            query = query.filter(Expense.is_planned == is_planned)
        if categories and is_planned is not None:
            query = query.filter(and_(Expense.category.in_(categories), Expense.is_planned == is_planned))
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
        categories = session.query(Expense.category, func.sum(Expense.cost)).\
                                                                filter(Expense.is_planned == is_planned).\
                                                                group_by(Expense.category).\
                                                                order_by(Expense.category).\
                                                                all()
        categories_dict = {category: cost for category, cost in categories}
        return categories_dict or {}
    
    def get_selected_countries(self):
        session = self.Session()
        return [row[0] for row in session.query(distinct(Expense.country)).all()]
    
class FixedDatabase:
    
    def __init__(self):
        self.fixed_engine = create_engine('sqlite:///databases/fixed_costs.db')
        # Only activate the following line to create the database
        # Base.metadata.create_all(self.fixed_engine, tables=[FixedCost.__table__])
        self.FixedSession = sessionmaker(bind=self.fixed_engine)
        self.table_name = FixedCost

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
    
class IncomeDatabase:
    
    def __init__(self) -> None:
        self.engine = create_engine('sqlite:///expenses.db')
        # Only activate the following line to create the database
        # Base.metadata.create_all(self.fixed_engine, tables=[FixedCost.__table__])
        self.FixedSession = sessionmaker(bind=self.engine)
        self.table_name = Income
