import json
from .token import token


def test_cart_list(app, client):
    mimetype = 'application/json'

    headers = {
        "Authorization":token,
        'Content-Type':mimetype,
        'Accept':mimetype
    }
    
    res = client.get("/api/cart", headers=headers)

    if res.status_code != 200:
        assert False
        
    res =  res.get_data()
    res = json.loads(res)

def test_add_to_cart(app, client):
    mimetype = 'application/json'

    headers = {
        "Authorization":token,
        'Content-Type':mimetype,
        'Accept':mimetype
    }
    data={
            "product":10
        }
    
    res = client.post("/api/cart", headers=headers, data=json.dumps(data))
    res = json.loads( res.get_data() )


    assert "message" in res

def test_delete_cart(app, client):
    
    mimetype = 'application/json'

    headers = {
        "Authorization":token,
        'Content-Type':mimetype,
        'Accept':mimetype
    }
    data={
        "id": 10
    }
    
    res = client.delete("/api/cart", data=json.dumps(data), headers=headers)
    print(res)
    

    res =  res.get_data()
    res = json.loads(res)
    
    
    assert "message" in res










