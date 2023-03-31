import pandas as pd

COUNTRIES = {
    "Südafrika": "South Africa",
    "Mauritius": "Mauritius",
    "Kenia": "Kenya",
    "Tansania": "Tanzania",
    "Israel": "Israel",
    "Ägypten": "Egypt",
    "Marokko": "Morocco",
    "VAE": "UAE",
    "Thailand": "Thailand",
    "Vietnam": "Vietnam",
    "Malaysia": "Malaysia",
    "Indonesien": "Indonesia",
    "Indien": "India",
    "Nepal": "Nepal",
    "Philippinen": "Philippines",
    "Japan": "Japan",
    "Mexiko": "Mexico",
    "Kuba": "Cuba",
    "Europa": "Europe",
    "Costa Rica": "Costa Rica",
    "Panama": "Panama",
    "Argentinien": "Argentina",
    "Chile": "Chile",
    "Brasilien": "Brazil",
    "Peru": "Peru",
    "Hawaii": "Hawaii",
    "Australien": "Australia",
    "Neuseeland": "New Zealand"
}

def data_frame_to_database(data: pd.DataFrame):
    data.drop(["amount", "localCurrency", "homeCurrency", "paymentMethod", "countryCode", "photoUrl", "place", "paidBy", "paidFor"], axis=1, inplace=True)
    data = data.rename(columns={"amountInHomeCurrency": "cost", "datePaid": "date", "notes": "name"})
    data["date"] = pd.to_datetime(data["date"], format='%d.%m.%Y')
    data["cost"] = data["cost"].str.replace(",", ".")
    data["category"] = data["category"].str.lower()
    """ for country in data["country"]:
        data["country"] = data["country"].replace(country, COUNTRIES[country]) """
    print(data.head())
    return data

def country_de_to_country_eng(country: str):
    return COUNTRIES[country]