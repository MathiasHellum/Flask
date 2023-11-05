from neo4j import GraphDatabase, Driver
from src.models.Driver import _get_connection
import re

class Car:
    def __init__(self, make, model, year, location, status):
        """Initialize a Car object with the provided attributes."""

        self.make = make
        self.model = model
        self.year = year
        self.location = location
        self.status = status


def list_of_cars():
    """Retrieve a list of all cars from the database."""

    driver = _get_connection()
    if driver:
        with driver.session() as session:
            try:
                result = session.run(
                    "MATCH (c:Car) RETURN ID(c) as id, c.make as make, c.model as model, c.year as year, c.location as location, c.status as status"
                )
                cars = [{
                        'id': record["id"],
                        'make': record["make"],
                        'model': record["model"],
                        'year': record["year"],
                        'location': record["location"],
                        'status': record["status"]
                    }
                    for record in result]
            except Exception as e:
                print(f"Error: {e}")
    else:
        print("The driver is not connected")
    return cars


def is_valid(id):
    """Checks if the given car ID is valid"""

    driver = _get_connection()
    if driver:
        with driver.session() as session:
            try:
                result = session.run(
                    "MATCH (c:Car) WHERE ID(c) = $id RETURN c",
                    id=id
                )
                return bool(result.single())  # Check if a result exists
            except Exception as e:
                print(f"Error: {e}")
                return False  # Return False on error
    return False  # Return False if the driver is not connected


def add_car(make,model,year,location,status):
    """Add a new car to the database with the provided details."""

    driver = _get_connection()
    if driver:
        with driver.session() as session:
            try:
                session.run(
                    "CREATE (c:Car {make: $make, model: $model, year: $year, location: $location, status: $status})",
                    make=make,
                    model=model,
                    year=year,
                    location=location,
                    status=status
                )
                print(f"Car added: Make - {make}, Model - {model}")
            except Exception as e:
                print(f"Error: {e}")
    else:
        print("The driver is not connected")


def update_car(id, newStatus):
    """Update the status of a car with the given ID to the new status."""

    if not is_valid(id):
        raise Exception(f"No car found with ID: {id}")
    
    driver = _get_connection()
    if driver:
        with driver.session() as session:
            try:
                result = session.run(
                    "MATCH (c:Car) WHERE ID(c) = $id SET c.status = $newStatus", 
                    id=id, 
                    newStatus=newStatus
                )
                summary = result.consume()
                if summary.counters.nodes_created == 0 and summary.counters.properties_set == 0:
                    print(f"No car found with ID: {id}")
                else:
                    print(f"Car with ID {id} updated with new status: {newStatus}")
            except Exception as e:
                print(f"Error: {e}")
    else:
        print("The driver is not connected")


def delete_car(id):
    """Delete a car with the given ID from the database."""
    
    if not is_valid(id):
        raise Exception(f"No car found with ID: {id}")
    
    driver = _get_connection()
    if driver:
        with driver.session() as session:
            try:
                session.run(
                    "MATCH (c:Car) WHERE ID(c) = $id DELETE c",
                    id=id
                )
            except Exception as e:
                print(f"Error: {e}")
    else:
        print("The driver is not connected")


def get_car_by_id(car_id):
    driver = _get_connection()
    if driver:
        with driver.session() as session:
            try:
                result = session.run(
                    "MATCH (c:Car) WHERE ID(c) = $car_id RETURN ID(c) as id, c.make as make, c.model as model, c.year as year, c.location as location, c.status as status",
                    car_id=car_id
                )
                record = result.single()
                if record:
                    car = {
                        'id': record["id"],
                        'make': record["make"],
                        'model': record["model"],
                        'year': record["year"],
                        'location': record["location"],
                        'status': record["status"]
                    }
                    return car
            except Exception as e:
                print(e)
    return None


def get_all_available_cars():
    driver = _get_connection()
    if driver:
        with driver.session() as session:
            try:
                result = session.run("MATCH (c:Car) WHERE c.status='available' RETURN ID(c) as id, c.make as make, c.model as model")
                cars = [{'id': record["id"], 'make': record["make"], 'model': record["model"]} for record in result]
                return cars
            except Exception as e:
                print(str(e))
    return []

