from src import app
from flask import render_template, request, redirect, url_for
from src.models.User import findUserByUsername


@app.route('/')
def landing_page():
    return render_template('landing_page.html.j2', title="Welcome!")


@app.route('/customer')
def customer_choices():
    return render_template('customer.html.j2')