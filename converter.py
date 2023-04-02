import pandas as pd


def data_frame_to_database(data: pd.DataFrame):
    data.drop(["amount", "localCurrency", "homeCurrency", "paymentMethod", "countryCode", "photoUrl", "place", "paidBy", "paidFor"], axis=1, inplace=True)
    data = data.rename(columns={"amountInHomeCurrency": "cost", "datePaid": "date", "notes": "name"})
    data["date"] = pd.to_datetime(data["date"], format='%d.%m.%Y')
    data["cost"] = data["cost"].str.replace(",", ".").astype(float)
    data["category"] = data["category"].str.lower()
    data["country"] = data["country"].str.lower().str.replace(" ", "")
    
    # assume your DataFrame is called df
    grouped = data.groupby('country')

    # create a dictionary of dictionaries, with each country as a key
    result_dict = {}
    for country, group in grouped:
        result_dict[country] = group.to_dict(orient='records')
    return result_dict
