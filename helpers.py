import requests
import os
if "APP_TOKEN" in os.environ:
    APP_TOKEN = os.environ['APP_TOKEN']
else:
    from config import APP_TOKEN

def format_queries(house_number, street_name, boro):

    boro = boro.upper()
    street_name = street_name.upper()
    street_address = ' '.join([house_number, street_name])
    jsons = {
            'hpd_violations': "wvxf-dwi5",
            'dob_violations': "3h2n-5cm9",
            'multiple_dwelling': "tesw-yqqr",
            'housing_litigation': "59kj-x8nc",
            'alt_enforcement': "hcir-3275",
            'no_harassment': "bzxi-2tsw",
            
            # get doc id from address, use doc id to get doc info
            'acris': "636b-3b5g", 
            
            # dunno
        #     'acris2': "bnx9-e6tj",
            
        }

    params = {
        'hpd_violations': {
            'boro': boro, 
            'streetname': street_name, 
            'housenumber': house_number
        },
        
        'dob_violations': {
            'street': street_name,
            'house_number': house_number
        },
        
        'multiple_dwelling': {
            'housenumber': house_number, 
            "streetname": street_name
        },
        'housing_litigation': {
            'housenumber': house_number, 
            "streetname": street_name
        },
        
        'alt_enforcement': {
            "street_address": street_name, 
            "phn": house_number
        },
        
        'no_harassment': {
            "street_address": street_address
        },
        
        # get doc id from address, use doc id to get doc info
        'acris': {
            "address_1": street_address
        }
        
        # dunno
    #     'acris2': "bnx9-e6tj",
        
    }

    return jsons, params

def q(json_, params, app_token=APP_TOKEN):
    url_base = "https://data.cityofnewyork.us/resource/"
    url = ''.join([url_base, json_, ".json"])
    r = requests.get(
        url, 
        headers={'X-App-Token': app_token}, 
        params=params)
    print(r)
    return r