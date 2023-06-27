import json

def test_product_list(app, client):
    res = client.get('/api/products')

    res_json = json.loads(res.get_data())
    for r in res_json:
        assert type(r["categories"]) == str
    
    assert len( res_json ) >= 1
    assert res.status_code == 200