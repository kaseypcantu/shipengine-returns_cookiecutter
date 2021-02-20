from flask import url_for
from flask_mail import Message

from kc_funk_returns import mail, ShipEngine


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(
            subject="You Return Shipping Label",
            sender="",
            recipients=[user.email],
    )

    msg.body = f"""To reset your password, visit the following link: 
{url_for("users.reset_token", token=token, _external=True)}

If you did not make this request, simply ignore this email and no changes will be made
"""
    return mail.send(msg)  # might not need return statement, need to debug to tell.


def send_shipping_label_email(email_addr: str, label_pdf: str):
    msg = Message(
            subject="Your Return Shipping Label",
            sender="",
            recipients=[email_addr]
    )

    msg.html = f"""<p>Your return shipping label is here! Please find it below as an attachment.</p>
        <ul>
            <li>Download the PDF attachment, or open it in your browser.<a herf="{label_pdf}" target=_blank></li>
            <li>Print your return shipping label with your preferred printer.</li>
            <li>Tape it to the shipment or box you are sending your items back in.</li>
            <li>Send it!</li>
        </ul>
    """

    # msg.attach(filename="return_shipping_label.pdf", content_type="application/pdf", data=label_pdf)

    return mail.send(msg)
