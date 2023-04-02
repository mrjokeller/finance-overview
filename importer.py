import pandas as pd
from database import CountryDatabase

def data_frame_to_database(data: pd.DataFrame):
    data.drop(["amount", "localCurrency", "homeCurrency", "paymentMethod", "countryCode", "photoUrl", "place", "paidBy", "paidFor"], axis=1, inplace=True)
    data = data.rename(columns={"amountInHomeCurrency": "cost", "datePaid": "date", "notes": "name"})
    # data["date"] = pd.to_datetime(data["date"], format='%d.%m.%Y')
    data["cost"] = data["cost"].str.replace(",", ".")
    data["category"] = data["category"].str.lower()
    data["country"] = data["country"].str.lower().str.replace(" ", "")
    
    # assume your DataFrame is called df
    grouped = data.groupby('country')

    # create a dictionary of dictionaries, with each country as a key
    result_dict = {}
    for country, group in grouped:
        result_dict[country] = group.to_dict(orient='records')
    return result_dict

def mass_import(path: str):
    data = pd.read_csv(path)
    clean_data = data_frame_to_database(data)
    for country, expenses in clean_data.items():
        database = CountryDatabase(country)
        for expense in expenses:
            print(f"Importing {expense['name']} to {country}...")
            successfully_added = database.add_expense(name=expense["name"], cost=expense["cost"], category=expense["category"], is_planned=False, date=expense["date"])
            if not successfully_added:
                print(f"Failed to import {expense['name']} to {country}.")
            else:
                print(f"Successfully imported {expense['name']} to {country}.")
