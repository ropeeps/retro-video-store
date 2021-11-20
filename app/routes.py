#from flask.helpers import make_response
from app import db
from flask import Blueprint, jsonify, request
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental 
from datetime import datetime, timedelta 

customers_bp = Blueprint("customers_bp", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos_bp", __name__, url_prefix="/videos")
rentals_bp = Blueprint("rentals_bp", __name__, url_prefix="/rentals")

#wave 1 
@videos_bp.route("", methods=["POST", "GET"])
def handle_videos():
    # POST REQUEST
    if request.method == "POST":
        video_request_body = request.get_json()
        
        if "title" not in video_request_body:
            return jsonify({"details": "Request body must include title."}), 400
        elif "release_date" not in video_request_body:
            return jsonify({"details": "Request body must include release_date."}), 400
        elif "total_inventory" not in video_request_body:
            return jsonify({"details": "Request body must include total_inventory."}), 400
    
        new_video = Video(
            title = video_request_body["title"],
            #release_date = video_request_body["release_date"],
            total_inventory = video_request_body["total_inventory"]
        )
        db.session.add(new_video)
        db.session.commit()
        new_video_response = new_video.get_video_dict()
        return jsonify(new_video_response), 201   
    # GET REQUEST
    elif request.method == "GET":
        video_title_query = request.args.get("title")
        if video_title_query:
            videos = Video.query.filter(Video.title.contains(video_title_query))
        else:
            videos = Video.query.all()
        video_response = []
        for video in videos:
            video_response.append(video.get_video_dict())
        
        if video_response == []:
            return jsonify(video_response), 200
        return jsonify(video_response), 200
 # GET, PUT, DELETE ONE VIDEO AT A TIME
@videos_bp.route("/<video_id>", methods=["GET", "PUT", "DELETE"])
def handle_one_video_at_a_time(video_id):
    if not video_id.isnumeric():
         return jsonify(None), 400
    request_body = request.get_json()

    video = Video.query.get(video_id)

    if not video:
        return jsonify({"message": f"Video {video_id} was not found"}), 404
    
    if request.method == "GET":
        return jsonify(video.get_video_dict()), 200
    elif request.method == "PUT":
        video_update_request_body = request.get_json()
        if "title" not in video_update_request_body:
            return jsonify(None), 400

        video.title = video_update_request_body["title"],
        video.release_date = video_update_request_body["release_date"],
        video.total_inventory = video_update_request_body["total_inventory"]

        db.session.commit()

        #updated_video_response = {video.get_video_dict()}
        updated_video_response = video.get_video_dict()

        return jsonify(updated_video_response), 200

    elif request.method == "DELETE":
        db.session.delete(video)
        db.session.commit()
        video_delete_response = video.get_video_dict()

        print("********", video_delete_response), 200
        return jsonify(video_delete_response), 200

# CUSTOMER ROUTES
@customers_bp.route("", methods=["GET", "POST"])
def handle_customers():
    # POST REQUEST
    if request.method == "POST":
        cust_request_body = request.get_json()
        if "name" not in cust_request_body:
            return jsonify({"details": "Request body must include name."}), 400
        elif "postal_code" not in cust_request_body:
            return jsonify({"details": "Request body must include postal_code."}), 400
        elif "phone" not in cust_request_body:
            return jsonify({"details": "Request body must include phone."}), 400
        new_customer = Customer(
            name = cust_request_body["name"],
            postal_code = cust_request_body["postal_code"],
            phone = cust_request_body["phone"]
        )
        db.session.add(new_customer)
        db.session.commit()
        new_cust_response = new_customer.get_cust_dict()
        
        return jsonify(new_cust_response), 201
    # GET REQUEST
    elif request.method == "GET":
        customer_name_query = request.args.get("name")
        customer_postal_query = request.args.get("postal_code")
        
        if customer_name_query:
            customers = Customer.query.filter(Customer.name.contains(customer_name_query))
        elif customer_postal_query:
            customers = Customer.query.filter(Customer.postal_code.contains(customer_postal_query))
        else:
            customers = Customer.query.all()
        customers_response = []
        for customer in customers:
            customers_response.append(customer.get_cust_dict())
        if customers_response == []:
            return jsonify(customers_response), 200

        print("**************")
        print(customers_response)
        return jsonify(customers_response), 200

 # GET, PUT, DELETE ONE CUSTOMER AT A TIME
@customers_bp.route("/<customer_id>", methods=["GET", "PUT", "DELETE"])
def handle_one_customer_at_a_time(customer_id):
    if not customer_id.isnumeric():
        return jsonify(None), 400

    customer = Customer.query.get(customer_id)

    if customer is None:
        return jsonify({"message": f"Customer {customer_id} was not found"}), 404

    if request.method == "GET":
        return jsonify(customer.get_cust_dict()), 200
        #return jsonify(customer.get_cust_dict()), 200 

    elif request.method == "PUT":
        put_request_body = request.get_json()
        if "name" not in put_request_body or "postal_code" not in put_request_body or "phone" not in put_request_body:
            return jsonify(None), 400

        customer.name = put_request_body["name"]
        customer.postal_code = put_request_body["postal_code"]
        customer.phone = put_request_body["phone"]
        customer.postal_code = put_request_body["postal_code"]

        db.session.commit()

        updated_customer_response = {
             "name": f"Updated ${customer.name}",
             "phone": f"Updated ${customer.phone}",
             "postal_code": f"Updated ${customer.postal_code}",
             "name": customer.name,
             "phone": customer.phone,
             "postal_code": customer.postal_code
         }

        return jsonify(updated_customer_response),  200
        #return jsonify(updated_customer_response), 200

    elif request.method == "DELETE":

        db.session.delete(customer)
        db.session.commit()


        if customer == []:
            cust_invalid_delete_response = {"message": f"Customer {customer_id} was not found"}

            return jsonify(cust_invalid_delete_response), 404
        else:
            cust_delete_response = customer.get_cust_dict()
            return jsonify(cust_delete_response), 200


#wave 2
@customers_bp.route("/<customer_id>/rentals", methods = ["GET"])
def videos_checked_out(customer_id):
    if not customer_id.isnumeric():
        return jsonify(None), 400

    video_list = []
    customer = Customer.query.get(customer_id)

    if not customer:
        return jsonify({"message": f"Customer {customer_id} was not found"}), 404

    current_customer_rentals = db.session.query(Rental).join(Customer.videos).filter(Customer.id == customer_id, Rental.is_checked_in == False)
    
    for rental in current_customer_rentals:
        video_list = [
        {
            "release_date": rental.video.release_date,
            "title": rental.video.title,
            "due_date": rental.due_date,
        }]
        
    return jsonify(video_list), 200


@rentals_bp.route("/check-out", methods=["POST"])
def handle_rental_check_outs():
    rentals_request_body = request.get_json()
    
    if "customer_id" not in rentals_request_body or "video_id" not in rentals_request_body:
        return jsonify(None), 400

    customer = Customer.query.get(rentals_request_body["customer_id"])
    if customer is None:
        return jsonify(None), 404

    video = Video.query.get(rentals_request_body["video_id"])
    if video is None:
        return jsonify(None), 404

    if video.total_inventory == 0:
        return jsonify({"message": "Could not perform checkout"}), 400
    db.session.query(Video).filter(Video.id == video.id).update({"total_inventory": (video.total_inventory - 1)})

    new_rental = Rental(
        customer_id=customer.id,
        video_id=video.id,
        is_checked_in=False
    )
    db.session.add(new_rental)
    db.session.commit()
    videos_checked_out = Rental.query.filter(Rental.customer_id == customer.id, Rental.video_id == video.id, Rental.is_checked_in == False).count()
    
    rental_receipt = {
        "customer_id": new_rental.customer_id,
        "video_id": new_rental.video_id,
        "due_date": new_rental.due_date,
        "videos_checked_out_count": videos_checked_out,
        "available_inventory": new_rental.video.total_inventory
        }
    return jsonify(rental_receipt), 200


@rentals_bp.route("/check-in", methods=["POST"])
def handle_video_check_ins():
    rentals_request_body = request.get_json()
    
    if "customer_id" not in rentals_request_body or "video_id" not in rentals_request_body:
        return jsonify(None), 400

    customer = Customer.query.get(rentals_request_body["customer_id"])
    if customer is None:
        return jsonify(None), 404

    video = Video.query.get(rentals_request_body["video_id"])
    if video is None:
        return jsonify(None), 404
    
    rental = Rental.query.filter(Rental.customer_id == rentals_request_body["customer_id"], Rental.video_id == rentals_request_body["video_id"], Rental.is_checked_in == False).first()
    if rental is None:
        return jsonify({"message": f"No oustanding rentals for customer {customer.id} and video {video.id}"}), 400

    updated_inventory = db.session.query(Video).filter(Video.id == video.id).update({"total_inventory": (video.total_inventory + 1)})
    db.session.query(Rental).filter(Rental.customer_id == customer.id, Rental.video_id == video.id).update({"due_date": (None), "is_checked_in": (True)})
    db.session.commit()

    still_checked_out = Rental.query.filter(Rental.customer_id == customer.id, Rental.is_checked_in == False).count()

    rental_receipt = {
            "customer_id": customer.id,
            "video_id": video.id,
            "videos_checked_out_count": still_checked_out,
            "available_inventory": updated_inventory
            }
    return jsonify(rental_receipt), 200


@videos_bp.route("/<video_id>/rentals", methods=["GET"])
def customers_who_checked_out(video_id):
    #return a list of customers who currently have the video checked out
    if not video_id.isnumeric():
        return jsonify(None), 400
    video = Video.query.get(video_id)
    if video is None:
        return jsonify({"message": f"Video {video_id} was not found"}), 404
    # Telling query to return both customer and rental
    results = db.session.query(Customer, Rental).filter(Rental.video_id == video.id, Rental.is_checked_in == False).all()
    customer_list = [
        {
            "due_date": rental.due_date,
            "name": customer.name,
            "phone": customer.phone,
            "postal_code": customer.postal_code
        } 
        for customer, rental in results
    ]
    
    return jsonify(customer_list), 200



# OPTIONAL ENHANCEMENT (Overdue Endpoint)
# --------------------------------------
@rentals_bp.route("/overdue", methods=["GET"])
def handle_overdue_rentals():
    # list all customers with overdue rentals
    sort_query = request.args.get("sort")
    if sort_query:
        customer = Customer.query.order_by(Customer.id.asc())
        customer = Customer.query.order_by(Customer.name.asc())
        customer = Customer.query.order_by(Customer.postal_code.asc())
        video = Video.query.order_by(Video.id.asc())
        video = Video.query.order_by(Video.title.asc())
        rental = Rental.query.order_by(Rental.due_date.asc())
    else:
        customer = Customer.query.all()
        video = Video.query.all()
        rental = Rental.query.all()
            
    now = datetime.today() + timedelta(days=14) #mock time
    overdue_rentals = Rental.query.filter(Rental.due_date < now).all()

    cust_overdue_list = [
         {
             "video_id": rental.video_id,
             "title": rental.video.title,
             "customer_id": rental.customer_id,
             "postal_code": customer.postal_code,
             "name": rental.customer.name,
             "postal_code": rental.customer.postal_code,
             "due_date": rental.due_date
             }
 
             for rental in overdue_rentals
             ]

    return jsonify(cust_overdue_list), 200