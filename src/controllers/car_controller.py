from src import app
from neo4j import GraphDatabase, Driver, AsyncGraphDatabase, AsyncDriver
import re
from src.models.Car import list_of_cars, add_car, update_car, delete_car
from flask import Flask, render_template, redirect, request, jsonify


@app.route('/cars')
def car_overview():
    try:
        data = list_of_cars()
        if not data:
            return render_template('cars.html.j2', data=data)  # Display an empty page if no cars found
    except Exception as e:
        error_message = f"An error occurred: {e}"
        return render_template('error.html.j2', error_message=error_message)
    return render_template('cars.html.j2', data=data)


@app.route('/cars/add', methods=["GET", "POST"])
def add_car_route():
    if request.method == "POST":
        make = request.form["make"]
        model = request.form["model"]
        year = request.form["year"]
        location = request.form["location"]
        status = request.form["status"]
        
        # Validate inputs
        if not make or not model or not year or not location or not status:
            error_message = "All fields are required."
            return render_template('add_car.html.j2', error_message=error_message)    
        try:
            add_car(make,model,year,location,status)
            # Redirect to car overview page after successful addition
            return redirect('/cars')
        except Exception as e:
            error_message = f"Error: {e}"
            return render_template('add_car.html.j2', error_message=error_message)
    return render_template('add_car.html.j2')


@app.route('/cars/update', methods=["GET", "POST"])
def update_car_route():
    if request.method == "POST":
        id = int(request.form["id"])
        newStatus = request.form["newStatus"]
        try:
            update_car(id, newStatus)
            data = list_of_cars()
            return render_template('cars.html.j2', data=data)
        except Exception as e:
            print(f"Error: {e}")
    return render_template('update_car.html.j2')


@app.route('/cars/delete', methods=["GET", "POST"])
def delete_car_route():
    if request.method == "POST":
        id = int(request.form["id"])
        try:
            delete_car(id)
            data = list_of_cars()
            #return jsonify(data)
            return render_template('cars.html.j2', data=data)
        except Exception as e:
            print(f"Error: {e}")
    return render_template('delete_car.html.j2')


@app.route('/cars/delete', methods=["GET", "POST"])
def delete_car_from_list_route():
    if request.method == "POST":
        id = int(request.form["id"])
        try:
            delete_car(id)
            data = list_of_cars()
            #return jsonify(data)
            return render_template('cars.html.j2', data=data)
        except Exception as e:
            print(f"Error: {e}")
    return render_template('delete_car.html.j2')



# @app.route('/customers')
# def customer_index():
#     data = []
#     try:
#         data = listCustomers()
#     except Exception as e:
#         print (f"Error: {e}")
#     return jsonify(data)
#     return render_template('cars.html.j2', data = data)

# @app.route('/customers/list')
# def customer_list():
#     data = []
#     try:
#         data = listCustomers()
#     except Exception as e:
#         print (f"Error: {e}")
#     return render_template('customers.html.j2', data = data)

# @app.route('/customers/add', methods=["GET", "POST"])
# def add_customer():
#     data = []
#     if request.method == "POST":
#         name = request.form["name"]
#         age = request.form["age"]
#         address = request.form["address"]
#         try:
#             addCustomer(name,age,address)
#             data = listCustomers()
#         except Exception as e:
#             print(f"Error {e}")
#         return jsonify(data)
#         return render_template('customers.html.j2', data=data)
#     return render_template('add_customer.html.j2')

# @app.route('/customers/update', methods=["GET", "POST"])
# def update_customer():
#     if request.method == "POST":
#         id = int(request.form["id"])
#         newAddress = request.form["newAddress"]
#         try:
#             updateCustomer(id, newAddress)
#             data = listCustomers()
#             return jsonify(data)    
#         except Exception as e:
#             print(f"Error: {e}")
#     return render_template('update_customer.html.j2')

# @app.route('/customers/delete', methods=["GET", "POST"])
# def delete_customer():
#     if request.method == "POST":
#         id = int(request.form["id"])
#         try:
#             deleteCustomer(id)
#             data = listCustomers()
#             return jsonify(data)
#         except Exception as e:
#             print(f"Error: {e}")
#     return render_template('delete_customer.html.j2')

# @app.route('/customers/list/delete', methods=["GET", "POST"])
# def delete_customer_from_list():
#     if request.method == "POST":
#         id = int(request.form["id"])
#         try:
#             deleteCustomer(id)
#             data = listCustomers()
#             return render_template('customers.html.j2', data=data)
#         except Exception as e:
#             print(f"Error: {e}")
#     return render_template('delete_customer.html.j2')

# @app.route('/employees')
# def employee_index():
#     data = []
#     try:
#         data = listEmployees()
#     except Exception as e:
#         print (f"Error: {e}")
#     return jsonify(data)
#     return render_template('employees.html.j2', data = data)

# @app.route('/employees/list')
# def employee_list():
#     data = []
#     try:
#         data = listEmployees()
#     except Exception as e:
#         print (f"Error: {e}")
#     return render_template('employees.html.j2', data = data)

# @app.route('/employees/add', methods=["GET", "POST"])
# def add_employee():
#     data = []
#     if request.method == "POST":
#         name = request.form["name"]
#         address = request.form["address"]
#         branch = request.form["branch"]
#         try:
#             addEmployee(name,address,branch)
#             data = listEmployees()
#         except Exception as e:
#             print(f"Error {e}")
#         return jsonify(data)
#         return render_template('employees.html.j2', data=data)
#     return render_template('add_employee.html.j2')

# @app.route('/employees/update', methods=["GET", "POST"])
# def update_employee():
#     if request.method == "POST":
#         id = int(request.form["id"])
#         newBranch = request.form["newBranch"]
#         try:
#             updateEmployee(id, newBranch)
#             data = listEmployees()
#             return jsonify(data)    
#         except Exception as e:
#             print(f"Error: {e}")
#     return render_template('update_employee.html.j2')

# @app.route('/employees/delete', methods=["GET", "POST"])
# def delete_employee():
#     if request.method == "POST":
#         id = int(request.form["id"])
#         try:
#             deleteEmployee(id)
#             data = listEmployees()
#             return jsonify(data)
#         except Exception as e:
#             print(f"Error: {e}")
#     return render_template('delete_customer.html.j2')

# @app.route('/employees/list/delete', methods=["GET", "POST"])
# def delete_employees_from_list():
#     if request.method == "POST":
#         id = int(request.form["id"])
#         try:
#             deleteEmployee(id)
#             data = listEmployees()
#             return render_template('employees.html.j2', data=data)
#         except Exception as e:
#             print(f"Error: {e}")
#     return render_template('delete_employees.html.j2')