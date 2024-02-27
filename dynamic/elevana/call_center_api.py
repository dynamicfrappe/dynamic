### test elevan call center 

import requests 

import json 


url = "https://integration.mersany.com:60004/api/v2/core/click_to_call"

api_key = "10231059fa6ad88d97b9aceb97993ee9"

body = {
       "caller": "120",
      "callee": "01205554644",
      "cos_id": 1 ,
      "cid_name": "Displayed Customer Name ",
      "cid_number": "01205554644"
}

r = requests.post(url , headers={"app-key" : api_key} , data=body ,verify=False)
print(r.status_code)
print(r.text)