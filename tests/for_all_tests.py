import requests
import json

# запрос с токеном
def test_with_auth(name, **kwargs):
    r = requests.post("http://127.0.0.1:5000/tokens", verify=False,auth=('admin', '12345'))
    if(r.status_code == 200):
        js = json.loads(r.content)
        if(js["success"]):
            token = js["result"]
            print(name)
            kwargs.update({"verify":False,  "headers":{"Authorization":f"Bearer {token}"}})
            r = requests.get(**kwargs)
            if(r.status_code == 200):
                print( json.loads(r.content))
            else:
                print(r.status_code)
            
    else:
        print("error auth, code: ", r.status_code)


def test_with_auth_put(name, **kwargs):
    r = requests.post("http://127.0.0.1:5000/tokens", verify=False,auth=('admin', '12345'))
    if(r.status_code == 200):
        #print(json.loads(r.content))
        js = json.loads(r.content)
        if(js["success"]):
            token = js["result"]
            print(name)
            kwargs.update({"verify":False,  "headers":{"Authorization":f"Bearer {token}"}})
            r = requests.put(**kwargs)
            if(r.status_code == 200):
                #print(r.status_code)
                print(json.loads(r.content))
            else:
                print(r.status_code)
            
    else:
        print("error auth, code: ", r.status_code)


def test_with_auth_add(name, **kwargs):
    r = requests.post("http://127.0.0.1:5000/tokens", verify=False,auth=('admin', '12345'))
    if(r.status_code == 200):
        #print(json.loads(r.content))
        js = json.loads(r.content)
        if(js["success"]):
            token = js["result"]
            print(name)
            kwargs.update({"verify":False,  "headers":{"Authorization":f"Bearer {token}"}})
            r = requests.put(**kwargs)
            if(r.status_code == 200):
                #print(r.status_code)
                print(json.loads(r.content))
            else:
                print(r.status_code)
            
    else:
        print("error auth, code: ", r.status_code)