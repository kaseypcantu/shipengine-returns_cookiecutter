import dataclasses

from flask import render_template, Blueprint, request, flash, jsonify

from {{cookiecutter.module_name}} import ShipEngine
from {{cookiecutter.module_name}}.main_routes.forms import ShippingAddressForm, SchedulePickupForm
from {{cookiecutter.module_name}}.models import ShipToAddress, ShipFromAddress, Package, PackageWeight, PackageDimensions

main = Blueprint("main", __name__)

se = ShipEngine()


@main.route("/", methods=["GET", "POST"])
def home():
    form = ShippingAddressForm()
    if request.method == "GET":
        return render_template("returns_portal.html", title="{{cookiecutter.project_name}}", form=form)
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
            phone="{{cookiecutter.return_to_phone_number}}",
            company_name="{{cookiecutter.return_to_name}}",
            address_line1="{{cookiecutter.return_address_line1}}",
            address_line2="{{cookiecutter.return_address_line2}}",
            address_line3="{{cookiecutter.return_address_line3}}",
            city_locality="{{cookiecutter.return_city}}",
            state_province="{{cookiecutter.return_state}}",
            postal_code="{{cookiecutter.return_postal_code}}",
            country_code="{{cookiecutter.return_country_code}}",
            address_residential_indicator="{{cookiecutter.return_residential_indicator}}"
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

    se_data = se.create_label(ship_to_address=shipToAddress, ship_from_address=shipFromAddress, packages=packages)
    status_code = se_data["status_code"]
    # label_pdf = se_data["shipengine_response"]["label_download"]["pdf"]

    # Uncomment line 75 if you have added SMTP credentials to the .env file so you can email the user their return shipping label
    # send_shipping_label_email(email_addr=form.contact_email.data, label_pdf=label_pdf)

    if int(str(status_code)[0]) == 5:
        print(se_data)
        return render_template("errors/se-5XX.html", title="{{cookiecutter.project_name}} - SE Error", error_data=se_data)
    elif int(str(status_code)[0]) == 4:
        print(se_data)
        return render_template("errors/se-4XX.html", title="{{cookiecutter.project_name}} - SE Error", error_data=se_data)

    flash('Label Generated!', "success")
    pickup_form = SchedulePickupForm()
    return render_template("return_label.html", title="Print Return Label", se_data=se_data, form=pickup_form)


