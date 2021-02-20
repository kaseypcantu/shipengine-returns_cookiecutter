import dataclasses
import datetime
import json
import logging
import os
from typing import List

import requests
from dotenv import load_dotenv
from flask import jsonify, flash
from requests import HTTPError
from requests.auth import AuthBase

from flask_server_funko_returns.models import (
    ShipFromAddress,
    ShipToAddress,
    Package,
    CustomsOptions,
    Shipment,
    AdvancedOptions,
    RateOptions,
)

load_dotenv()

logging.basicConfig(level=logging.DEBUG)

dt = datetime.datetime.now()


class ShipEngineAuth(AuthBase):
    def __init__(self, api_key):
        self.api_key = api_key

    def __call__(self, request):
        request.headers["API-Key"] = self.api_key
        return request


class ShipEngine:
    _BASE_URL = "https://api.shipengine.com/v1/"
    _CURRENT_DATE = dt.strftime("%m/%d/%Y")

    def __init__(
            self,
            api_key: str = os.getenv("SHIPENGINE_SANDBOX_API_KEY"),
            carrier_id: str = os.getenv("SHIPENGINE_CARRIER-ID"),
            carrier_service_code: str = os.getenv("SHIPENGINE_CARRIER_SERVICE_CODE")
    ):
        self.api_key = api_key
        self.carrier_id = carrier_id
        self.carrier_service_code = carrier_service_code
        self.session = requests.Session()

    def request(self, method: str, endpoint: str, *args, **kwargs):
        kwargs["auth"] = ShipEngineAuth(self.api_key)

        try:
            resp = self.session.request(
                    method, self._BASE_URL + endpoint.strip("/"), *args, **kwargs
            )
            # resp.raise_for_status()
            logging.debug(
                "SHIPENGINE_RESPONSE:\n" + json.dumps(resp.json(), indent=4)
            )  # logging response

            # Uncomment the following line for easy debug output on the response from ShipEngine API
            # r = {
            #     "status_code": resp.status_code,
            #     "shipengine_response": resp.json()
            # }
            return resp.json(), str(resp.status_code)
        except HTTPError as e:
            error_obj = [err["message"] for err in e.response.json()["error_routes"]]
            json_error_obj = jsonify(error_obj)
            flash(f"Label Creation Error: {json_error_obj}", "warn")
            logging.debug(
                    f"Request Failed: {resp.status_code} | e: {e}\n\n ERROR: {json.dumps(error_obj, indent=4)}\n"
            )
            return e, json_error_obj

    def get(self, endpoint, *args, **kwargs):
        return self.request("GET", endpoint, *args, **kwargs)

    def post(self, endpoint, *args, **kwargs):
        return self.request("POST", endpoint, *args, **kwargs)

    def update(self, endpoint, *args, **kwargs):
        return self.request("UPDATE", endpoint, *args, **kwargs)

    def delete(self, endpoint, *args, **kwargs):
        return self.request("DELETE", endpoint, *args, **kwargs)

    def create_shipment(
            self,
            ship_to_address: ShipToAddress,
            ship_from_address: ShipFromAddress,
            packages: List[Package],
            customs: CustomsOptions = None,
            advanced_opt: AdvancedOptions = None
            # shipments: List[Shipment]
    ):
        shipment = Shipment(
                carrier_id=self.carrier_id,
                service_code=self.carrier_service_code,
                validate_address="validate_and_clean",
                external_shipment_id=None,
                external_order_id=None,
                items=None,
                ship_date=self._CURRENT_DATE,
                ship_to=dataclasses.asdict(ship_to_address),
                ship_from=dataclasses.asdict(ship_from_address),
                warehouse_id=None,
                return_to=None,
                confirmation="delivery",
                customs=customs,
                advanced_options=advanced_opt,
                insurance_provider="none",
                packages=[dataclasses.asdict(package) for package in packages],
        )

        if advanced_opt is not None:
            shipment.advanced_options = dataclasses.asdict(advanced_opt)

        if customs is not None:
            shipment.customs = dataclasses.asdict(customs)

        # request = {"shipments": [dataclasses.asdict(shipment) for shipment in shipments]}
        request = { "shipments": [dataclasses.asdict(shipment)] }
        return self.post("shipments", json=request)

    def get_rates(self, shipment_id: str, rate_opt: RateOptions):
        request = {
            "shipment_id":  shipment_id,
            "rate_options": dataclasses.asdict(rate_opt),
        }
        return self.post("rates", json=request)

    def get_label_by_id(self, rate_id: str):
        return self.post(f"/labels/rates/{rate_id}")

    def create_label(
            self,
            ship_to_address: ShipToAddress,
            ship_from_address: ShipFromAddress,
            packages: List[Package],
            customs: CustomsOptions = None,
            advanced_opt: AdvancedOptions = None,
    ):

        shipment = Shipment(
                carrier_id=self.carrier_id,
                service_code=self.carrier_service_code,
                validate_address="validate_and_clean",
                external_shipment_id=None,
                external_order_id=None,
                items=None,
                ship_date=self._CURRENT_DATE,
                ship_to=dataclasses.asdict(ship_to_address),
                ship_from=dataclasses.asdict(ship_from_address),
                warehouse_id=None,
                return_to=None,
                confirmation="none",
                customs=customs,
                advanced_options=advanced_opt,
                insurance_provider="none",
                packages=[dataclasses.asdict(package) for package in packages],
        )

        if advanced_opt is not None:
            shipment.advanced_options = dataclasses.asdict(advanced_opt)

        if customs is not None:
            shipment.customs = dataclasses.asdict(customs)

        request = { "shipment": dataclasses.asdict(shipment) }
        return self.post("labels", json=request)

# user_ship_from = ShipFromAddress(
#         name="Monkey D. Luffy",
#         phone="1-654-987-3124",
#         company_name="The Grand Line",
#         address_line1="3800 N Lamar Blvd",
#         address_line2="Ste 220",
#         address_line3=None,
#         city_locality="Austin",
#         state_province="TX",
#         postal_code="78756",
#         country_code="US",
#         address_residential_indicator="no"
# )
#
# curative_ship_to = ShipToAddress(
#         name="Kasey Cantu",
#         phone="1-789-456-1234",
#         company_name="ShipEngine",
#         address_line1="4009 Marathon Blvd",
#         address_line2="Suite 100",
#         address_line3=None,
#         city_locality="Austin",
#         state_province="TX",
#         postal_code="78756",
#         country_code="US",
#         address_residential_indicator="no"
# )
#
# weight = PackageWeight(
#         value=3,
#         unit="ounce"
# )
#
# dims = PackageDimensions(
#         unit="inch",
#         length=0,
#         width=0,
#         height=0
# )
#
# package_1 = Package(
#         weight=dataclasses.asdict(weight),
#         dimensions=dataclasses.asdict(dims),
#         package_code="package"
# )
#
#
# se = ShipEngine()
#
# r = se.create_label(ship_to_address=curative_ship_to,
#                     ship_from_address=user_ship_from,
#                     packages=[package_1])
#
# print(r[0]["label_id"])
# print(r[1])
# p.pprint(r["shipments"][0]["shipment_id"])
# p.pprint(r)
