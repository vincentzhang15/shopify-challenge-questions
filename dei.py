# Developer Intern Challenge Question
# Requirements:
#   Basic CRUD Functionality. You should be able to:
#     Create inventory items
#     Edit Them
#     Delete Them
#     View a list of them

#   ONLY ONE OF THE FOLLOWING (We will only evaluate the first feature chosen, so please only choose one)
#     When deleting, allow deletion comments and undeletion
#     Ability to create warehouses/locations and assign inventory to specific locations
#     Ability to create “shipments” and assign inventory to the shipment, and adjust inventory appropriately
#   Authentication and CSS/Design are not required and will not be considered during evaluation.

import logging
from flask import current_app, flash, Flask, Markup, redirect, render_template, make_response
from flask import request, url_for
from flask import send_from_directory

from front import front_page
import os

from app import app


@app.route('/dei')
def dei_site():
    return front_page("dei","")

@app.route('/dei/create', methods=['GET', 'POST'])
def dei_create():
    return front_page("dei","")

@app.route('/dei/edit', methods=['GET', 'POST'])
def dei_edit():
    return front_page("dei","")

@app.route('/dei/delete', methods=['GET', 'POST'])
def dei_delete():
    return front_page("dei","")


