from app import db
from flask import Blueprint, jsonify, request
from app.models.customer import Customer
from app.models.video import Video
from datetime import datetime
import os

customers_bp = Blueprint("customers_bp", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos_bp", __name__, url_prefix="/videos")


#wave 1 customer routes
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






#wave 1 video routes
@videos_bp.route("", methods=["POST", "GET"])
def handle_videos():
<<<<<<< Updated upstream
    pass






@videos_bp.route("/<video_id>", methods=["GET", "PUT", "DELETE"])
def handle_one_video_at_a_time(video_id):
    pass
=======
    if request.method == "GET":
        # sort_title_query = request.args.get("sort_by_title")
        # sort_id_query = request.args.get("sort_by_id")
        # sort_release_date_query = request.args.get("sort_by_release_date")
        # if sort_title_query == "desc":
        #     video = Video.query.order_by(Video.title.desc())
        # elif sort_title_query == "asc":
        #     video = Video.query.order_by(Video.title.asc())
        # if sort_id_query == "desc":
        #     video = Video.query.order_by(Video.id.desc())
        # elif sort_id_query == "asc":
        #     video = Video.query.order_by(Video.id.asc())
        # if sort_release_date_query == "asc":
        #     video = Video.query.order_by(Video.release_date.asc())
        # if sort_release_date_query == "desc":
        #     video = Video.query.order_by(Video.release_date.desc())
        # else:
        video = Video.query.all()
        if not video:
            response_body = {
                "message": f"Video {video.id} was not found"
            }
            return jsonify(response_body), 404
        videos_response = []
        for video in video: 
            videos_response.append(video.get_video_dict)
            return jsonify(videos_response), 200
        if request.method == "POST":
            request_body = request.get_json()
            if "title" or "release_date" or "total_inventory" not in request_body:
                return{
                    "400": "Bad Request"
                }, 400
            response_body = {
                "id": video.id
            }
        return jsonify("201: Created", response_body), 201
    

@videos_bp.route("/<video_id>", methods=["GET", "PUT", "DELETE"])
def handle_one_video_at_a_time(video_id):
    video = Video.query.get(video_id)
    request_body = request.get_json()
    if not video:
            response_body = {
                "message": f"Video {video_id} was not found"
            }
            return jsonify(response_body), 404
    elif request.method == "GET":
        if video not in video.get_video_dict: 
            return jsonify("400 Bad Request"), 400
        response_body = video.get_video_dict
        return jsonify(response_body), 200
    elif request.method == "PUT":
        if "title" or "release_date" or "total_inventory" not in request_body:
            return jsonify("400 Bad Request"), 400 
        video.title = request_body["title"]
        video.release_date = request_body["release_date"]
        video.total_inventory = request_body["total_inventory"]
        db.session.commit()
        response_body = {video.get_video_dict}
        return jsonify(response_body), 200
    elif request.method == "DELETE":
        db.session.delete(video)
        db.session.commit()
        response_body = {
            "id": video.id
        }
        return jsonify(response_body), 200
>>>>>>> Stashed changes
