from src import app
from neo4j import GraphDatabase, Driver, AsyncGraphDatabase, AsyncDriver
import re
from src.models.Car import list_of_cars, add_car, update_car, delete_car, is_valid
from flask import Flask, render_template, redirect, request, jsonify


@app.route('/cars')
def car_overview():
    """Displays an overview of cars stored in the database.\n    
    Displays an empty page if no cars are found, or an error page in case of an exception.
    """

    try:
        data = list_of_cars()
        if not data:
            return render_template('car_templates/cars.html.j2', data=data)  # Display an empty page if no cars found
    except Exception as e:
        error_message = f"An error occurred: {e}"
        return render_template('error.html.j2', error_message=error_message)
    return render_template('car_templates/cars.html.j2', data=data)


@app.route('/cars/add', methods=["GET", "POST"])
def add_car_route():
    """Handles the route for adding a new car to the database.\n    
    Displays an error message if required fields are missing or if an exception occurs during car addition.
    """
    if request.method == "POST":
        make = request.form["make"]
        model = request.form["model"]
        year = request.form["year"]
        location = request.form["location"]
        status = request.form["status"]
        
        # Validate inputs
        if not make or not model or not year or not location or not status:
            error_message = "All fields are required."
            return render_template('car_templates/add_car.html.j2', error_message=error_message)    
        try:
            add_car(make,model,year,location,status)
            # Redirect to car overview page after successful addition
            return redirect('/cars')
        except Exception as e:
            error_message = f"Error: {e}"
            return render_template('car_templates/add_car.html.j2', error_message=error_message)
    return render_template('car_templates/add_car.html.j2')


@app.route('/cars/update', methods=["GET", "POST"])
def update_car_route():
    """Handles the route for updating car information in the database.\n    
    Displays an error message if the provided car ID is invalid, new status is missing, or if an exception occurs.
    """
    if request.method == "POST":
        try:
            id = int(request.form["id"])
            newStatus = request.form["newStatus"]

            # Validate inputs
            if not newStatus:
                error_message = "New Status is required."
                return render_template('car_templates/update_car.html.j2', error_message=error_message)
            
            if not is_valid(id):
                error_message = "No car found with the given ID."
                return render_template('car_templates/update_car.html.j2', error_message=error_message)

            update_car(id, newStatus)
            return redirect('/cars')  # Redirect to car overview page after successful update

        except ValueError:
            error_message = "Invalid ID. Please enter a valid ID."
            return render_template('car_templates/update_car.html.j2', error_message=error_message)

        except Exception as e:
            error_message = f"An error occurred: {e}"
            return render_template('error.html.j2', error_message=error_message)

    return render_template('car_templates/update_car.html.j2')


@app.route('/cars/delete', methods=["GET", "POST"])
def delete_car_route():
    """Handles the route for deleting a car from the database.\n    
    Displays an error message if the provided car ID is invalid, or if an exception occurs.
    """
    if request.method == "POST":
        try:
            id = int(request.form["id"])

            if not is_valid(id):
                error_message = "No car found with the given ID."
                return render_template('car_templates/delete_car.html.j2', error_message=error_message)

            delete_car(id)
            return redirect('/cars')  # Redirect to car overview page after successful update

        except ValueError:
            error_message = "Invalid ID. Please enter a valid ID."
            return render_template('car_templates/delete_car.html.j2', error_message=error_message)

        except Exception as e:
            error_message = str(e)  # Display the error message
            return render_template('car_templates/delete_car.html.j2', error_message=error_message)

    return render_template('car_templates/delete_car.html.j2')
