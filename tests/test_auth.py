import json

def test_fail_login(app, client):
    res = client.post("/api/login", data={
        "email":"cruzlemuel5@gmail.com",
        "password": "dsadsad"
        })
    
    
    print(res.status_code)
    res= json.loads(res.get_data() )
    
    print(res)
    
 
    assert "Error" in res[0]

def tets_success_login(app, client):
    res = client.post("/api/login", data={
        "email":"cruzlemuel0@gmail.com",
        "password": "pppppppppppp"
    })
    
    
    res_json = json.loads( res.get_data() )  
    
    assert "access_token" in res_json == True


def test_fail_register(app, client):
    data={
        "first_name":"Lemuel",
        "last_name":"cruz",
        "password":"pppppppppppp",
        "email": "cruzlemuel0@gmail.com"
    }
    
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    
    res = client.post("/api/register", data=json.dumps(data), headers=headers)
    
    

    assert res.status_code == 400

# def test_success_register(app, client):
    
#     data={
#         "first_name":"Lemuel",
#         "last_name":"cruz",
#         "password":"pppppppppppp",
#         "email": "cruzlemuel89999@gmail.com"
#     }
#     mimetype = 'application/json'
#     headers = {
#         'Content-Type': mimetype,
#         'Accept': mimetype
#     }
#     res = client.post(
#         "/api/register", 
#         data=json.dumps(data), 
#         headers=headers
#     )
   

#     assert res.status_code == 200
    
