from flask import Blueprint, render_template, jsonify, request

from flask_server_funko_returns import ShipEngine

se = ShipEngine()

api = Blueprint("api", __name__)


class APIError(Exception):
    """Represents an API error.
        Follows the API exception raising and handling pattern documented
        at http://flask.pocoo.org/docs/0.12/patterns/apierrors/
    """
    def __init__(self, status_code, payload):
        super(APIError, self).__init__(self)
        self.status_code = status_code
        self.payload = payload


@api.errorhandler(APIError)
def handle_api(error):
    """Responds with an API error in JSON format.
        Parameters
        ----------
        error: APIError
        Returns
        -------
        dict
    """
    response = jsonify(error.payload)
    response.status_code = error.status_code

    return response


@api.route("/schedule-pickup", methods=["POST"])
def schedule_pickup():
    reqForm = request.form
    data = {
        "label_ids":       [
            reqForm["label_id"]
        ],
        "contact_details": {
            "name":  reqForm["contact_name"],
            "email": reqForm["contact_email"],
            "phone": reqForm["contact_phone"]
        },
        "pickup_notes":    reqForm["pickup_notes"],
        "pickup_window":   {
            "start_at": reqForm["pickup_window_start_at"],
            "end_at":   reqForm["pickup_window_end_at"]
        }
    }

    se_pickup = se.post("/pickups", json=data)
    status_code = se_pickup["status_code"]

    if int(str(status_code)[0]) == 5:
        print(se_pickup)
        return render_template("errors/se-5XX.html", title="flask server funko Returns Portal - SE Error",
                               error_data=se_pickup)
    elif int(str(status_code)[0]) == 4:
        print(se_pickup)
        return render_template("errors/se-4XX.html", title="flask server funko Returns Portal - SE Error",
                               error_data=se_pickup)

    print(se_pickup)
    return render_template("scheduled_pickup.html", pickup_resp=se_pickup)


@api.route("/scheduled-pickup", methods=["GET"])
def scheduled_pickup_page():
    return NotImplemented


@api.route("/cancel-pickup/<string:pickup_id>", methods=["DELETE"])
def cancel_pickup(pickup_id):
    cancelled_pickup = se.delete(f"/pickups/{pickup_id}")
    return jsonify({
        "cancelled_pickup_id": cancelled_pickup.pickup_id
    }), 200


@api.route("/ping/<string:user>", methods=["GET"])
def ping(user):
    return jsonify({
        "se_returns": "pong",
        "hello":      user
    }), 200
