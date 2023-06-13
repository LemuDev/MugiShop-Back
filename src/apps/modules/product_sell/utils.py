import requests
from decouple import config

# get the order payed (Link for pay)
def getOrder(id_order):
    token = get_paypal_token()
    token = token["access_token"]
    
    
    headers = {
        'Accept' : 'application/json',
        'Content-Type' : 'application/json',
        'PayPal-Request-Id': config("PAYPAL_REQUEST_ID"),
        'Authorization':  'Bearer ' + token
    }
    
    response = requests.post(f'{ config("URL_GET_ORDER") }/{ id_order }/capture', headers=headers)
    response = response.json()
    
    
    return response

# Get the paypal token  
def get_paypal_token():
    auth = (config("CLIENT_ID"), config("CLIENT_SECRET") )
    
    data = {
        'grant_type': 'client_credentials',
    }
    
    response = requests.post(
        config("URL_GET_TOKEN"), 
        data=data, 
        auth=auth
    )
    
    response = response.json()    
    return response

