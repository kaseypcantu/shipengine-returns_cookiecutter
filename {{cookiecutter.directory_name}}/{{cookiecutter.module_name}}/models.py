from dataclasses import dataclass
from enum import Enum, unique
from typing import List, Optional


@dataclass
class ShipFromAddress:
    name: str
    phone: str
    company_name: Optional[str]
    address_line1: str
    address_line2: Optional[str]
    address_line3: Optional[str]
    city_locality: str
    state_province: str
    postal_code: str
    country_code: str
    address_residential_indicator: str

    def __post_init__(self):
        valid_residential_indicators = ("yes", "no", "unknown")
        if self.address_residential_indicator not in valid_residential_indicators:
            raise ValueError(
                    f"address_residential_indicator must be on of {valid_residential_indicators}"
            )


@dataclass
class ShipToAddress:
    name: str
    phone: str
    company_name: Optional[str]
    address_line1: str
    address_line2: Optional[str]
    address_line3: Optional[str]
    city_locality: str
    state_province: str
    postal_code: str
    country_code: str
    address_residential_indicator: str  # Might change to ENUM

    def __post_init__(self):
        valid_residential_indicators = ("yes", "no", "unknown")
        if self.address_residential_indicator not in valid_residential_indicators:
            raise ValueError(
                    f"address_residential_indicator must be on of {valid_residential_indicators}"
            )


@dataclass
class ReturnAddress:
    name: str
    phone: str
    company_name: Optional[str]
    address_line1: str
    address_line2: Optional[str]
    address_line3: Optional[str]
    city_locality: str
    state_province: str
    postal_code: str
    country_code: str
    address_residential_indicator: str  # Might change to ENUM

    def __post_init__(self):
        valid_residential_indicators = ("yes", "no", "unknown")
        if self.address_residential_indicator not in valid_residential_indicators:
            raise ValueError(
                    f"address_residential_indicator must be on of {valid_residential_indicators}"
            )


@dataclass
class Items:
    name: str
    sales_order_id: Optional[str]
    sales_order_item_id: Optional[str]
    quantity: int
    sku: Optional[str]
    external_order_id: Optional[str]
    asin: Optional[str]
    order_source_code: str  # Might change to ENUM

    def __post_init__(self):
        valid_order_sources = (
            "amazon_ca",
            "amazon_us",
            "brightpearl",
            "channel_advisor",
            "cratejoy",
            "ebay",
            "etsy",
            "jane",
            "groupon_goods",
            "magento",
            "paypal",
            "seller_active",
            "shopify",
            "stitch_labs",
            "squarespace",
            "three_dcart",
            "tophatter",
            "walmart",
            "woo_commerce",
            "volusion",
        )
        if self.order_source_code not in valid_order_sources:
            raise ValueError(f"order_source_code must be one of {valid_order_sources}")


@dataclass
class RateOptions:
    carrier_ids: List[str]
    package_types: List[str]
    service_codes: List[str]
    calculate_tax_amount: bool
    preferred_currency: str  # Might change to ENUM

    def __post_init__(self):
        valid_currencies = ("usd", "cad", "aud", "gbp", "eur", "nzd")
        if self.preferred_currency not in valid_currencies:
            raise ValueError(f"preferred_currency must be one of {valid_currencies}")


@dataclass
class CustomsValue:
    currency: str  # Might change to ENUM
    amount: float

    def __post_init__(self):
        valid_currencies = ("usd", "cad", "aud", "gbp", "eur", "nzd")
        if self.currency not in valid_currencies:
            raise ValueError(f"currency must be one of {valid_currencies}")


@dataclass
class CustomsItem:
    description: Optional[str]
    quantity: int
    value: Optional[List[CustomsValue]]


@dataclass
class CustomsOptions:
    contents: str  # Might change to ENUM
    non_delivery: str  # Might change to ENUM
    customs_items: Optional[List[CustomsItem]]
    harmonized_tariff_code: Optional[str]
    country_of_origin: Optional[str]

    def __post_init__(self):
        valid_contents = (
            "merchandise",
            "documents",
            "gift",
            "returned_goods",
            "sample",
        )
        if self.contents not in valid_contents:
            return ValueError(f"contents must be one of {valid_contents}")

        non_delivery_options = ("return_to_sender", "treat_as_abandoned")
        if self.non_delivery not in non_delivery_options:
            raise ValueError(f"non_delivery must be one of {non_delivery_options}")


@dataclass
class DryIceWeight:
    value: int
    unit: str  # Might change to ENUM

    def __post_init__(self):
        valid_units = ("pound", "ounce", "gram", "kilogram")
        if self.unit not in valid_units:
            raise ValueError(f"weight unit must be one of {valid_units}.")


@dataclass
class PaymentAmount:
    currency: str  # Might change to ENUM
    amount: float

    def __post_init__(self):
        valid_currencies = ("usd", "cad", "aud", "gbp", "eur", "nzd")
        if self.currency not in valid_currencies:
            raise ValueError(f"currency must be one of {valid_currencies}")


@dataclass
class CollectOnDelivery:
    payment_type: str  # Might change to ENUM
    payment_amount: PaymentAmount

    def __post_init__(self):
        valid_payment_types = ("any", "cash", "cash_equivalent", "none")
        if self.payment_type not in valid_payment_types:
            raise ValueError(f"payment_type must be one of {valid_payment_types}")


@dataclass
class PackageWeight:
    value: float
    unit: str  # Might change to ENUM

    def __post_init__(self):
        valid_units = ("pound", "ounce", "gram", "kilogram")
        if self.unit not in valid_units:
            raise ValueError(f"weight unit must be one of {valid_units}.")


@dataclass
class PackageDimensions:
    unit: str
    length: float
    width: float
    height: float

    def __post_init__(self):
        valid_units = ("inch", "centimeter")
        if self.unit not in valid_units:
            raise ValueError(f"dimension unit must be one of {valid_units}.")


@dataclass
class PackageInsuredValue:
    currency: str
    amount: float


@dataclass
class PackageLabelMessages:
    reference1: str
    reference2: str
    reference3: str


@dataclass
class Package:
    weight: PackageWeight
    dimensions: Optional[PackageDimensions]
    package_code: Optional[str] = None
    insured_value: Optional[PackageInsuredValue] = None
    label_messages: Optional[PackageLabelMessages] = None
    external_package_id: Optional[str] = None


@dataclass
class AdvancedOptions:
    bill_to_account: Optional[str]
    bill_to_country_code: Optional[str]
    bill_to_party: Optional[str]
    bill_to_postal_code: Optional[str]
    contains_alcohol: Optional[bool]
    delivery_duty_paid: Optional[bool]
    dry_ice: Optional[str]
    dry_ice_weight: Optional[DryIceWeight]
    non_machinable: Optional[bool]
    saturday_delivery: Optional[bool]
    custom_field1: Optional[str]
    custom_field2: Optional[str]
    custom_field3: Optional[str]
    collect_on_delivery: Optional[CollectOnDelivery]


@dataclass
class Shipment:
    carrier_id: str
    service_code: str
    validate_address: Optional[str]
    external_order_id: Optional[str]
    items: Optional[List[Items]]  # Might change to ENUM
    external_shipment_id: Optional[str]
    ship_date: str
    ship_to: ShipToAddress
    ship_from: ShipFromAddress
    warehouse_id: Optional[str]
    return_to: Optional[ReturnAddress]
    confirmation: str  # Might make an ENUM
    customs: Optional[List[CustomsOptions]]
    advanced_options: Optional[AdvancedOptions]
    insurance_provider: str  # Might change to ENUM
    packages: List[Package]

    def __post_init__(self):
        confirmation_options = (
            "none",
            "delivery",
            "signature",
            "adult_signature",
            "direct_signature",
            "delivery_mailed",
        )
        if self.confirmation not in confirmation_options:
            return ValueError(f"confirmation must be one of {confirmation_options}")

        # valid_order_sources = ("amazon_ca", "amazon_us", "brightpearl",
        #                        "channel_advisor", "cratejoy", "ebay",
        #                        "etsy", "jane", "groupon_goods", "magento",
        #                        "paypal", "seller_active", "shopify",
        #                        "stitch_labs", "squarespace", "three_dcart",
        #                        "tophatter", "walmart", "woo_commerce", "volusion")
        # if self.order_source_code not in valid_order_sources:
        #     raise ValueError(f"order_source_code must be one of {valid_order_sources}")


@unique
class SupportedCurrencies(Enum):
    usd = 1
    cad = 2
    aud = 3
    gbp = 4
    eur = 5
    nzd = 6


@dataclass
class SchedulePickupContactDetails:
    name: str
    email: str
    phone: str


@dataclass
class PickupWindow:
    start_at: str
    end_at: str


@dataclass()
class SchedulePickupRequest:
    label_ids: [str]
    contact_details: SchedulePickupContactDetails
    pickup_notes: str
    pickup_window: PickupWindow
