from config.config import CONF
from fastapi import APIRouter
import requests
import xmltodict
import json

check_router = APIRouter()

@check_router.get(
    "/{id_}",
    response_model=dict
)
async def get_contact_by_id(id_: str):
    _xml = f'<CityStateLookupRequest USERID="{CONF["usps"]["userID"]}"><ZipCode ID=\'0\'><Zip5>{id_}</Zip5></ZipCode></CityStateLookupRequest>'
    r = requests.get(
            f"https://production.shippingapis.com/ShippingAPI.dll?API= CityStateLookup&XML={_xml}"
            
        )
    decoded_response = r.content.decode("utf-8")
    response_json = json.loads(json.dumps(xmltodict.parse(decoded_response)))
    city = response_json['CityStateLookupResponse']['ZipCode']['City'].title()
    state = response_json['CityStateLookupResponse']['ZipCode']['State']
    return {"city": city, "state": state}
    
    
