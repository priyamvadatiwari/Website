import nasdaqdatalink
import pandas as pd
import json
import urllib.request

nasdaqdatalink.ApiConfig.api_key = 'BX5mXxH8WZy8xdayYB1a'

def get_data():
    
    countries = ["CAN","IND","UKR","TUR"]
    
    data_list = []
    
    for country in countries:
        data = nasdaqdatalink.get(f'ECONOMIST/BIGMAC_{country}', start_date='2021-01-31', end_date='2022-01-31')
        # print(data)
        if country == "ROC":
            country = "TWN"
            
        url = f'https://restcountries.com/v3.1/alpha/{country}'
        request = urllib.request.urlopen(url)
        result = json.loads(request.read())
        # print(result)

        if country == "TWN":
            country = "ROC"
        
    
        country = {
        "country":country,
        "local_price": data.iloc[0,0],
        "dollar_ex": data.iloc[0,1],
        "dollar_price": data.iloc[0,2],
        "dollar_ppp": data.iloc[0,3],
        "dollar_valuation":data.iloc[0,4],
        "dollar_adj_valuation":data.iloc[0,5],
        "flag":result[0]["flags"]["png"],
        "country_name":result[0]["name"]["common"],
        "currencies":result[0]["currencies"],
        }
        data_list.append(country)

        number = float(round(data.iloc[0,3],2))
        #print(number, type(number))
        burger = "🍔" * (int(number))
        data_list.append(burger)
        data_list.append(int(number))
        print(data_list)
    
    
    return data_list
