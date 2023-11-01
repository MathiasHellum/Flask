from src import app
from src.models.Employee import list_of_employees, add_employee, update_employee, delete_employee, is_valid_employee
from flask import render_template, redirect, request


@app.route('/employees')
def employee_overview():
    """Displays an overview of employees stored in the database.\n
    Displays an empty page if no employees are found, or an error page in case of an exception.
    """

    try:
        data = list_of_employees()
        if not data:
            return render_template('employee_templates/employees.html.j2', data=data)  # Display an empty page if no employees found
    except Exception as e:
        error_message = f"An error occurred: {e}"
        return render_template('error.html.j2', error_message=error_message)
    return render_template('employee_templates/employees.html.j2', data=data)


@app.route('/employees/add', methods=["GET", "POST"])
def add_employee_route():
    """Handles the route for adding a new employee to the database.\n
    Displays an error message if required fields are missing or if an exception occurs during employee addition.
    """

    if request.method == "POST":
        name = request.form["name"]
        address = request.form["address"]
        branch = request.form["branch"]

        # Validate inputs
        if not name or not address or not branch:
            error_message = "All fields are required."
            return render_template('employee_templates/add_employee.html.j2', error_message=error_message)

        try:
            add_employee(name, address, branch)
            return redirect('/employees')  # Redirect to employee overview page after successful addition
        except Exception as e:
            error_message = f"Error: {e}"
            return render_template('employee_templates/add_employee.html.j2', error_message=error_message)
    return render_template('employee_templates/add_employee.html.j2')


@app.route('/employees/update', methods=["GET", "POST"])
def update_employee_route():
    """Handles the route for updating employee information in the database.\n
    Displays an error message if the provided employee ID is invalid or if an exception occurs.
    """

    if request.method == "POST":
        try:
            id = int(request.form["id"])
            newName = request.form["newName"]
            newAddress = request.form["newAddress"]
            newBranch = request.form["newBranch"]

            # Validate inputs
            if not newName and not newAddress and not newBranch:
                error_message = "At least one of the new values (Name, Address, or Branch) is required."
                return render_template('employee_templates/update_employee.html.j2', error_message=error_message)

            if not is_valid_employee(id):
                error_message = "No employee found with the given ID."
                return render_template('employee_templates/update_employee.html.j2', error_message=error_message)

            update_employee(id, newName, newAddress, newBranch)
            return redirect('/employees')  # Redirect to employee overview page after successful update

        except ValueError:
            error_message = "Invalid ID. Please enter a valid ID."
            return render_template('employee_templates/update_employee.html.j2', error_message=error_message)

        except Exception as e:
            error_message = f"An error occurred: {e}"
            return render_template('error.html.j2', error_message=error_message)

    return render_template('employee_templates/update_employee.html.j2')


@app.route('/employees/delete', methods=["GET", "POST"])
def delete_employee_route():
    """Handles the route for deleting an employee from the database.\n
    Displays an error message if the provided employee ID is invalid, or if an exception occurs.
    """

    if request.method == "POST":
        try:
            id = int(request.form["id"])

            if not is_valid_employee(id):
                error_message = "No employee found with the given ID."
                return render_template('employee_templates/delete_employee.html.j2', error_message=error_message)

            delete_employee(id)
            return redirect('/employees')  # Redirect to employee overview page after successful deletion

        except ValueError:
            error_message = "Invalid ID. Please enter a valid ID."
            return render_template('employee_templates/delete_employee.html.j2', error_message=error_message)

        except Exception as e:
            error_message = str(e)  # Display the error message
            return render_template('employee_templates/delete_employee.html.j2', error_message=error_message)

    return render_template('employee_templates/delete_employee.html.j2')
