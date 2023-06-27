import json
from .token import token


def test_create_order(app, client):
    mimetype = 'application/json'

    headers_add_cart = {
        "Authorization":token,
        'Content-Type':mimetype,
        'Accept':mimetype
    }
    data={
            "product":7
        }
    
    res_add_cart = client.post("/api/cart", headers=headers_add_cart, data=json.dumps(data))


    headers = {
        "Authorization":token,
        'Content-Type':mimetype,
        'Accept':mimetype
    }
    
    res = client.post('/api/create-order', headers=headers)
    res = res.get_data()
    
    res = json.loads(res)
    
 
    
    assert 'link_pay' in res