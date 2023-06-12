import requests

# get the order payed (Link for pay)
def getOrder(id_order):
    token = get_paypal_token()
    token = token["access_token"]
    
    
    headers = {
        'Accept' : 'application/json',
        'Content-Type' : 'application/json',
        'PayPal-Request-Id': '7b92603e-77ed-4896-8e78-5dea2050476a',
        'Authorization':  'Bearer ' + token
    }
    
    response = requests.post(f'https://api-m.sandbox.paypal.com/v2/checkout/orders/{id_order}/capture', headers=headers)
    response = response.json()
    
    
    return response

# Get the paypal token  
def get_paypal_token():
    auth = ('AYJxnaEndV8YqpfEONJaUE3R07Qoetbn9O9Xpl_cX6Ii53sUuI4FH4pd-MruXY1pUO_Ai46oct9eDuO_', 'EIgOCaF8UM1LKuJy6XERI8ByZg3gTWAkhF_JaDfi_AiHclXTsRijTVGCvsy4Sse_mbzGXyRKBE1TcktF')
    
    

    data = {
        'grant_type': 'client_credentials',
    }

    response = requests.post(
        'https://api-m.sandbox.paypal.com/v1/oauth2/token', 
        data=data, 
        auth=auth
    )
    
    response = response.json()
        
    return response

