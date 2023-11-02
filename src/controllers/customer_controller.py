from src import app
from neo4j import GraphDatabase, Driver, AsyncGraphDatabase, AsyncDriver
import re
from src.models.Customer import list_of_customers, add_customer, update_customer, delete_customer, is_valid_customer, find_customer_by_name_and_phone
from flask import Flask, render_template, redirect, request, jsonify, url_for

@app.route('/customers')
def customer_overview():
    """Displays an overview of customers stored in the database."""

    try:
        data = list_of_customers()
        if not data:
            return render_template('customer_templates/customers.html.j2', data=data)
    except Exception as e:
        error_message = f"An error occurred: {e}"
        return render_template('error.html.j2', error_message=error_message)
    return render_template('customer_templates/customers.html.j2', data=data)

@app.route('/customers/add', methods=["GET", "POST"])
def add_customer_route():
    """Handles the route for adding a new customer to the database."""
    
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone_number = request.form["phone_number"]
        
        # Validate inputs
        if not name or not email or not phone_number:
            error_message = "All fields are required."
            return render_template('customer_templates/add_customer.html.j2', error_message=error_message)    

        try:
            add_customer(name, email, phone_number)
            return redirect('/customers')
        except Exception as e:
            error_message = f"Error: {e}"
            return render_template('customer_templates/add_customer.html.j2', error_message=error_message)

    return render_template('customer_templates/add_customer.html.j2')

@app.route('/customers/update', methods=["GET", "POST"])
def update_customer_route():
    """Handles the route for updating customer information in the database.
    
    Displays an error message if the provided customer ID is invalid, 
    or if any exception occurs during the update process.
    """
    if request.method == "POST":
        try:
            id = int(request.form["id"])
            # Add other fields you'd like to update for the customer. Here's an example:
            new_name = request.form["name"]

            # Validate inputs
            if not new_name:
                error_message = "New Name is required."
                return render_template('customer_templates/update_customer.html.j2', error_message=error_message)
            
            if not is_valid_customer(id):
                error_message = "No customer found with the given ID."
                return render_template('customer_templates/update_customer.html.j2', error_message=error_message)

            # Here, call the appropriate function to update the customer. For example:
            update_customer(id, new_name)
            
            return redirect('/customers')  # Redirect to customer overview page after successful update

        except ValueError:
            error_message = "Invalid ID. Please enter a valid ID."
            return render_template('customer_templates/update_customer.html.j2', error_message=error_message)

        except Exception as e:
            error_message = f"An error occurred: {e}"
            return render_template('error.html.j2', error_message=error_message)

    return render_template('customer_templates/update_customer.html.j2')


@app.route('/customers/delete', methods=["GET", "POST"])
def delete_customer_route():
    """Handles the route for deleting a customer from the database."""

    if request.method == "POST":
        try:
            id = int(request.form["id"])

            if not is_valid_customer(id):  # Check if the customer ID is valid before attempting deletion
                error_message = "No customer found with the given ID."
                return render_template('customer_templates/delete_customer.html.j2', error_message=error_message)

            delete_customer(id)
            return redirect('/customers')
        except ValueError:
            error_message = "Invalid ID. Please enter a valid ID."
            return render_template('customer_templates/delete_customer.html.j2', error_message=error_message)
        except Exception as e:
            error_message = str(e)
            return render_template('customer_templates/delete_customer.html.j2', error_message=error_message)

    return render_template('customer_templates/delete_customer.html.j2')


@app.route('/customer/login', methods=["GET", "POST"])
def customer_login():
    """Handles customer login by checking name and phone number."""
    if request.method == "POST":
        try:
            name = request.form["name"]
            phone_number = request.form["phone_number"]
            
            customer = find_customer_by_name_and_phone(name, phone_number)
            if customer:
                # TODO: Implement any session management or further login processes
                return jsonify({"message": "Logged in successfully!", "customer": customer})
            else:
                return render_template("customer_login.html.j2", error="Invalid credentials.")
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return render_template("customer_login.html.j2")

# @app.route('/customer/login', methods=["GET", "POST"])
# def customer_login():
#     if request.method == "GET":
#         return render_template("customer_login.html.j2")
    
#     elif request.method == "POST":
#         try:
#             name = request.form["name"]
#             phone_number = request.form["phone_number"]
            
#             customer = find_customer_by_name_and_phone(name, phone_number)
#             if customer:
#                 # TODO: Implement any session management or further login processes
#                 return jsonify({"message": "Logged in successfully!", "customer": customer})
#             else:
#                 return jsonify({"error": "Invalid credentials."}), 401
            
#         except Exception as e:
#             return jsonify({"error": str(e)}), 500


@app.route('/customer/register', methods=["GET", "POST"])
def customer_register():
    """Handles customer registration."""
    if request.method == "POST":
        try:
            name = request.form["name"]
            email = request.form["email"]
            phone_number = request.form["phone_number"]
            
            existing_customer = find_customer_by_name_and_phone(name, phone_number)
            if existing_customer:
                return render_template("customer_register.html.j2", error="Customer with given name and phone number already exists.")
            
            add_customer(name, email, phone_number)
            return redirect(url_for('customer_login'))
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return render_template("customer_register.html.j2")


# @app.route('/customer/login', methods=["POST"])
# def customer_login():
#     """Handles customer login by checking name and phone number."""
#     try:
#         name = request.form["name"]
#         phone_number = request.form["phone_number"]
        
#         customer = find_customer_by_name_and_phone(name, phone_number)
#         if customer:
#             # TODO: Implement any session management or further login processes
#             return jsonify({"message": "Logged in successfully!", "customer": customer})
#         else:
#             return jsonify({"error": "Invalid credentials."}), 401
        
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route('/customer/register', methods=["POST"])
# def customer_register():
#     """Handles customer registration."""
#     try:
#         name = request.form["name"]
#         email = request.form["email"]
#         phone_number = request.form["phone_number"]
        
#         existing_customer = find_customer_by_name_and_phone(name, phone_number)
#         if existing_customer:
#             return jsonify({"error": "Customer with given name and phone number already exists."}), 409
        
#         add_customer(name, email, phone_number)
#         return jsonify({"message": "Customer registered successfully!"})
    
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500