from src import app
from flask import jsonify, render_template, request
from src.models.Car import get_car_by_id, get_all_available_cars, is_valid, list_of_cars
from src.models.Customer import has_customer_booked_or_rented, book_car_for_customer, list_of_customers


@app.route('/order-car', methods=["GET"])
def show_order_car_form():
    all_cars = list_of_cars()
    available_cars = [car for car in all_cars if car["status"] == "available"]  # Filter only available cars
    customers = list_of_customers()

    return render_template("endpoints/order_car.html.j2", title="Order Car", cars=available_cars, customers=customers)



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
    return jsonify({"success": "Car booked successfully"}), 200
