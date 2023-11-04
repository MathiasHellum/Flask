from src import app
from flask import jsonify, redirect, render_template, request, url_for
from src.models.Car import get_car_by_id, get_all_available_cars, is_valid, list_of_cars, update_car, change_car_status
from src.models.Customer import has_customer_booked_or_rented, book_car_for_customer, list_of_customers, find_customer_by_name_and_phone, find_customer_by_id, cancel_booking_for_customer, return_car_for_customer
from src.controllers.customer_controller import get_booking_for_customer


@app.route('/order-car', methods=["GET"])
def show_order_car_form():
    name = request.args.get("name")
    phone_number = request.args.get("phone_number")
    selected_customer = find_customer_by_name_and_phone(name, phone_number)

    all_cars = list_of_cars()
    available_cars = [car for car in all_cars if car["status"] == "available"]  # Filter only available cars

    return render_template("endpoints/order_car.html.j2", cars=available_cars, selected_customer=selected_customer)



@app.route('/order-car', methods=["POST"])
def order_car():

    customer_id = int(request.form["customer_id"])
    car_id = int(request.form["car_id"])


    if not get_car_by_id(car_id):
        return jsonify({"error": "Invalid car ID"}), 400

    car = get_car_by_id(car_id)
    if car['status'] != "available":
        return jsonify({"error": "Car is not available"}), 400

    if has_customer_booked_or_rented(customer_id):
        return jsonify({"error": "Customer has already booked a car"}), 400

    book_car_for_customer(car_id, customer_id)
    customer_details = find_customer_by_id(customer_id)
    if customer_details:
        name = customer_details['name']
        phone_number = customer_details['phone_number']
        return redirect(url_for("customer_info", name=name, phone_number=phone_number))
    #return jsonify({"success": "Car booked successfully"}), 200


@app.route('/cancel-booking', methods=["GET"])
def show_cancel_booking_form():
    name = request.args.get("name")
    phone_number = request.args.get("phone_number")
    selected_customer = find_customer_by_name_and_phone(name, phone_number)

    booked_car = get_booking_for_customer(selected_customer['id'])
    if not booked_car:
        return "No booking found for this customer", 404

    return render_template("endpoints/cancel_booking.html.j2", booking=booked_car, selected_customer=selected_customer)

@app.route('/cancel-booking', methods=["POST"])
def cancel_booking():
    customer_id = int(request.form["customer_id"])
    success = cancel_booking_for_customer(customer_id)
    customer_details = find_customer_by_id(customer_id)
    name = customer_details['name']
    phone_number = customer_details['phone_number']
    if success:
        return redirect(url_for('customer_info', name=name, phone_number=phone_number))
    else:
        return "Failed to cancel booking", 500



@app.route('/rent-car', methods=["POST"])
def rent_car():
    customer_id = request.form.get("customer_id")
    car_id = request.form.get("car_id")

    # Check if the customer_id and car_id are provided
    if not customer_id or not car_id:
        return jsonify({"error": "Customer ID or Car ID is missing."}), 400

    customer_id = int(customer_id)
    car_id = int(car_id)

    # Check if the car is available for renting
    car = get_car_by_id(car_id)
    if not car:
        return jsonify({"error": "Invalid car ID"}), 400

    if car['status'] != "booked":
        return jsonify({"error": "Car is not available for rent"}), 400


    # Change the car's status to 'rented'
    try:
        update_car(car_id, "rented")
        customer_details = find_customer_by_id(customer_id)
        if customer_details:
            name = customer_details['name']
            phone_number = customer_details['phone_number']
            return redirect(url_for("customer_info", name=name, phone_number=phone_number))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/return-car', methods=["POST"])
def return_car():
    # Check if the customer_id is provided
    customer_id = int(request.form["customer_id"])
    if not customer_id:
        return jsonify({"error": "Customer ID is missing."}), 400
    
    try:
        success = cancel_booking_for_customer(customer_id)

    except ValueError as e:
        # Handle specific errors like car not being rented by the customer
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        # Handle any unexpected errors
        return jsonify({"error": "An error occurred while returning the car."}), 500

    customer_details = find_customer_by_id(customer_id)
    name = customer_details['name']
    phone_number = customer_details['phone_number']

    if success:
        return redirect(url_for('customer_info', name=name, phone_number=phone_number))
    else:
        return "Failed to cancel booking", 500

