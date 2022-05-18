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
import mysql.connector

from front import front_page
import os

from app import app
import dbconn
dbconn = dbconn.dbconn

@app.route('/bdi')
def bdi_list():
    db = dbconn()
    cursor = db.cursor()
    cursor.execute(f"select id, name, category, price, amount, date_created, last_updated from bdiInventoryItems where state=0 order by last_updated desc, id desc limit 100;")
    result = cursor.fetchall()
    items = []
    for x in result:
        print(x)
        items += [{'id':x[0], 'name':x[1], 'category':x[2], 'price':x[3], 'amount':x[4], 'created':x[5], 'updated':x[6] }]
    cursor.close()

    print("-------------------------------------")
    print(items)

    return front_page("bdi_list",items=items)

@app.route('/bdi/create', methods=['GET', 'POST'])
def bdi_create():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)
        error = ""
        if len(data['name'])<1:
            error = "Please input the field \"Name\""
        elif len(data['category'])<1:
            error = "Please input the field \"Category\""
        elif len(data['price'])<1:
            error = "Please input the field \"Price\""
        elif len(data['amount'])<1:
            error = "Please input the field \"Amount\""
        
        if len(error) > 0:
            return front_page("bdi_create", error=error)

        values = (data['name'], data['category'], data['price'], data['amount'])

        try:
            db = dbconn()
            cursor = db.cursor()
            cursor.execute("insert into `bdiInventoryItems` ( `name`, `category`, `price`, `amount` ) values ( %s, %s, %s, %s)" , values )
            db.commit()
            items = getBdiItem()
            return front_page("bdi_item",items=items,title="Create Inventory Item", info="Item created.")

        except mysql.connector.Error as err:
            error = err
            return front_page("bdi_create", error=error)

    return front_page("bdi_create")

def getBdiItem(item_id=""):
    db = dbconn()
    cursor = db.cursor()
    if len(item_id) < 1:
        sql = "select id, name, category, price, amount, date_created, last_updated, comment from bdiInventoryItems order by id desc limit 1 ;"
    else:
        sql = "select id, name, category, price, amount, date_created, last_updated, comment from bdiInventoryItems where id=" + str(item_id) + " limit 1 ;"
    cursor.execute(sql)
    result = cursor.fetchall()
    items = []
    for x in result:
        print(x)
        items += [{'id':x[0], 'name':x[1], 'category':x[2], 'price':x[3], 'amount':x[4], 'created':x[5], 'updated':x[6], 'comment':x[7] }]
    cursor.close()
    return items

@app.route('/bdi/<item_id>/edit', methods=['GET', 'POST'])
def bdi_edit(item_id):
    items = getBdiItem(item_id)
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)
        error = ""
        if len(data['name'])<1:
            error = "Please input the field \"Name\""
        elif len(data['category'])<1:
            error = "Please input the field \"Category\""
        elif len(data['price'])<1:
            error = "Please input the field \"Price\""
        elif len(data['amount'])<1:
            error = "Please input the field \"Amount\""
        items[0]['name'] = data['name']
        items[0]['category'] = data['category']
        items[0]['price'] = data['price']
        items[0]['amount'] = data['amount']
        
        if len(error) > 0:
            return front_page("bdi_edit",items=items, error=error)

        values = (data['name'], data['category'], data['price'], data['amount'])

        try:
            db = dbconn()
            cursor = db.cursor()
            sql = "update `bdiInventoryItems` set `name`=%s, `category`=%s, `price`=%s, `amount`=%s, `last_updated`=CURRENT_TIME where `id`="+str(item_id)
            print(sql)
            cursor.execute(sql , values )
            db.commit()
            return front_page("bdi_item",items=items,title="Edit Inventory Item", info="Item updated.")

        except mysql.connector.Error as err:
            error = err
            return front_page("bdi_edit",items=items, error=error)

    return front_page("bdi_edit",items=items)

@app.route('/bdi/<item_id>/delete', methods=['GET', 'POST'])
def bdi_delete(item_id):
    items = getBdiItem(item_id)
    if request.method == 'POST':
        try:
            db = dbconn()
            cursor = db.cursor()
            # cursor.execute("delete from `bdiInventoryItems` where `id`="+str(item_id))
            data = request.form.to_dict(flat=True)
            values=[]
            values +=[data['comment']]
            values +=[str(item_id)]
            sql = "update `bdiInventoryItems` set `state`=1, `comment`=%s, `last_updated`=CURRENT_TIME where `id`=%s"
            cursor.execute(sql , values )
            db.commit()
            return front_page("bdi_item",items=items,title="Delete Inventory Item", info="Item deleted.")

        except mysql.connector.Error as err:
            error = err
            return front_page("bdi_delete",items=items, error=error)

    return front_page("bdi_delete",items=items)


@app.route('/bdi/undel')
def bdi_list_for_undelete():
    db = dbconn()
    cursor = db.cursor()
    cursor.execute(f"select id, name, category, price, amount, comment, date_created, last_updated from bdiInventoryItems where state=1 order by last_updated desc, id desc limit 100;")
    result = cursor.fetchall()
    items = []
    for x in result:
        items += [{'id':x[0], 'name':x[1], 'category':x[2], 'price':x[3], 'amount':x[4], 'comment':x[5], 'created':x[6], 'updated':x[7] }]
    cursor.close()

    return front_page("bdi_list_for_undel",items=items)

@app.route('/bdi/<item_id>/undelete', methods=['GET', 'POST'])
def bdi_undelete(item_id):
    items = getBdiItem(item_id)
    if request.method == 'POST':
        try:
            db = dbconn()
            cursor = db.cursor()
            values=[]
            values +=[str(item_id)]
            sql = "update `bdiInventoryItems` set `state`=0, `last_updated`=CURRENT_TIME where `id`=%s"
            cursor.execute(sql , values )
            db.commit()
            return front_page("bdi_item",items=items,title="Undelete Inventory Item", info="Item undeleted.")

        except mysql.connector.Error as err:
            error = err
            return front_page("bdi_undelete",items=items, error=error)

    return front_page("bdi_undelete",items=items)
