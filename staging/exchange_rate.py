import requests
import pycountry

currency_list = list(pycountry.currencies)
currencies = {}
for c in currency_list:
        currencies[c.alpha_3] = c.name


def get_exchange_rate(date, foreign_currency):

    """
    INPUT:
        date: string in format '2008-11-04'
        currency: string in format 'Turkish Lira'
    OUTPUT:
        returns appropriate historical exchange rate as json (?)
    """

    api_key = 'f3c2a32e73c4784284b8ca33a4f30f95'

    #returns 'TRY' from 'Turkish Lira' given as foreign_currency
    foreign_currency_code = list(currencies.keys())[list(currencies.values()).index(foreign_currency)]

    params = {'access_key': api_key, 'date': date, 'currencies': foreign_currency_code, 'format': 1}

    # use 'live' in place of historical if desired
    r = requests.get('http://apilayer.net/api/historical', params = params)

    usd_to_foreign_currency = 'USD' + foreign_currency_code

    # is returned as float by default
    historical_quote = r.json()['quotes'][usd_to_foreign_currency]
    print(type(historical_quote))
    return historical_quote

print(get_exchange_rate('2008-11-04', 'Turkish Lira'))