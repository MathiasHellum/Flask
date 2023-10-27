from neo4j import GraphDatabase, Driver
from src.models.Driver import _get_connection
import re

class Car:
    def __init__(self, make, model, year, location, status):
        self.make = make
        self.model = model
        self.year = year
        self.location = location
        self.status = status


def list_of_cars():
    cars = []
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
                #print(cars)
            except Exception as e:
                print(f"Error: {e}")
    else:
        print("The driver is not connected")
    return cars


def add_car(make,model,year,location,status):
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
    driver = _get_connection()
    if driver:
        with driver.session() as session:
            try:
                result = session.run(
                    "MATCH (c:Car) WHERE ID(c) = $id SET c.status = $newStatus", 
                    id=id, 
                    newStatus=newStatus
                )
                if result.summary().counters.updates == 0:
                    print(f"No car found with ID: {id}")
                else:
                    print(f"Car with ID {id} updated with new status: {newStatus}")
            except Exception as e:
                print(f"Error: {e}")
    else:
        print("The driver is not connected")


def delete_car(id):
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
