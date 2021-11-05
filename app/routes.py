from app import db
from flask import Blueprint, jsonify, request
from app.models.customer import Customer
from app.models.video import Video
from datetime import datetime
import os

customers_bp = Blueprint("customers_bp", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos_bp", __name__, url_prefix="/videos")


@customers_bp.route("", methods=["GET", "POST"])
def handle_customers():
    if request.method == "GET":
        customer_name_query = request.args.get("name")
        customer_postal_query = request.args.get("postal_code")
        customers = Customer.query.all()

        customers_response = []
        for customer in customers:
            customers_response.append(customer.get_cust_dict())

        if customers_response == []:
            return jsonify(customers_response), 200

    elif request.method == "POST":
        cust_request_body = request.get_json()
        if "name" not in cust_request_body or "postal_code" not in cust_request_body or "phone" not in cust_request_body:
            return jsonify({"details": "Invalid data"}), 400

        new_customer = Customer(
            name = cust_request_body["name"],
            postal_code = cust_request_body["postal_code"],
            phone = cust_request_body["phone"]
        )

        db.session.add(new_customer)
        db.session.commit()

        new_cust_response = {
            "Request body must include postal_code.": new_customer.get_cust_dict()
        }

        return jsonify(new_cust_response), 201

    





@customers_bp.route("/<customer_id>", methods=["GET", "PUT", "DELETE"])
def handle_one_customer_at_a_time(customer_id):
    pass






@videos_bp.route("", methods=["POST", "GET"])
def handle_videos():
    pass






@videos_bp.route("/<video_id>", methods=["GET", "PUT", "DELETE"])
def handle_one_video_at_a_time(video_id):
    pass