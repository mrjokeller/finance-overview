import pandas as pd
from database import CountryDatabase

def data_frame_to_database(data: pd.DataFrame):
    data.drop(["amount", "localCurrency", "homeCurrency", "paymentMethod", "countryCode", "photoUrl", "place", "paidBy", "paidFor", "type"], axis=1, inplace=True)
    data = data.rename(columns={"amountInHomeCurrency": "cost", "datePaid": "date", "notes": "name"})
    # data["date"] = pd.to_datetime(data["date"], format='%d.%m.%Y')
    data["cost"] = data["cost"].str.replace(",", ".").str.strip()
    data["category"] = data["category"].str.lower().str.strip()
    data["country"] = data["country"].str.lower().str.strip()

    data = data.to_dict(orient='records')
    return data

def mass_import(path: str):
    data = pd.read_csv(path)
    clean_data = data_frame_to_database(data)
    database = CountryDatabase()
    for expense in clean_data:
        print(f"Importing {expense['name']} to database...")
        successfully_added = database.add_expense(name=expense["name"], country=expense["country"], cost=expense["cost"], category=expense["category"], is_planned=False, date=expense["date"])
        if not successfully_added:
            print(f"Failed to import {expense['name']} to database.")
        else:
            print(f"Successfully imported {expense['name']} to database.")
