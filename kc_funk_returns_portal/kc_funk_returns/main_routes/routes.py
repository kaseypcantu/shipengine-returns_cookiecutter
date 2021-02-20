import json
import dataclasses

from flask import render_template, Blueprint, request, flash

from kc_funk_returns import ShipEngine
from kc_funk_returns.main_routes.forms import ShippingAddressForm, SchedulePickupForm
from kc_funk_returns.models import ShipToAddress, ShipFromAddress, Package, PackageWeight, PackageDimensions

main = Blueprint("main", __name__)

se = ShipEngine()


@main.route("/", methods=["GET", "POST"])
def home():
    form = ShippingAddressForm()
    if request.method == "GET":
        return render_template("returns_portal.html", title="kc funk Returns Portal", form=form)
    if not form.validate_on_submit():
        flash("Some fields you entered are invalid, please try check them and try again.", "danger")
        return render_template("returns_portal.html", form=form)
    shipToAddress = ShipToAddress(
            name=form.name.data,
            phone=form.phone.data,
            company_name=form.company_name.data,
            address_line1=form.address_line_1.data,
            address_line2=form.address_line_2.data,
            address_line3=form.address_line_3.data,
            city_locality=form.city_locality.data,
            state_province=form.state_province.data,
            postal_code=form.postal_code.data,
            country_code=form.country_code.data,
            address_residential_indicator=form.address_residential_indicator.data
    )

    shipFromAddress = ShipFromAddress(
            name="Kasey Cantu",
            phone="1-234-567-8910",
            company_name="John Doe",
            address_line1="4009 Marathon Blvd.",
            address_line2="Ste 100",
            address_line3="1st Floor",
            city_locality="Austin",
            state_province="TX",
            postal_code="78756",
            country_code="US",
            address_residential_indicator="no"
    )

    package_weight = PackageWeight(
            value=2.5,
            unit="ounce"
    )

    package_dimensions = PackageDimensions(
            unit="inch",
            length=5,
            width=5,
            height=5
    )

    packages = [
        Package(
                weight=dataclasses.asdict(package_weight),
                dimensions=dataclasses.asdict(package_dimensions),
                package_code="package"
        )
    ]

    se_response = se.create_label(ship_to_address=shipToAddress, ship_from_address=shipFromAddress, packages=packages)
    se_data, status_code = se_response
    # label_pdf = se_data["shipengine_response"]["label_download"]["pdf"]

    # Uncomment line 75 if you have added SMTP credentials to the .env file so you can email the user their return shipping label
    # send_shipping_label_email(email_addr=form.contact_email.data, label_pdf=label_pdf)

    if status_code[0] == "5":
        print(se_data)
        return render_template("errors/se-5XX.html", title="kc funk Returns Portal - SE Error", error_data=json.dumps(se_data, indent=2, separators=(",", ": ")), error_status=status_code)
    elif status_code[0] == "4":
        print(se_data)
        return render_template("errors/se-4XX.html", title="kc funk Returns Portal - SE Error", error_data=json.dumps(se_data, indent=2, separators=(",", ": ")), error_status=status_code)

    flash('Label Generated!', "success")
    pickup_form = SchedulePickupForm()
    return render_template("return_label.html", title="Print Return Label", se_data=se_data, form=pickup_form)


