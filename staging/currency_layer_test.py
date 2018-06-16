import requests

api_key = 'f3c2a32e73c4784284b8ca33a4f30f95'

params = {'access_key': api_key, 'date': '2008-11-04', 'currencies': 'USD,EUR,GBP,TRY', 'format': 1}

# use 'live' in place of historical if desired
r = requests.get('http://apilayer.net/api/historical', params = params)

historical_quote = r.json()

#print(historical_quote)

# get single quote
test = historical_quote['quotes']['USDTRY']

print(type(test))
print(test)
