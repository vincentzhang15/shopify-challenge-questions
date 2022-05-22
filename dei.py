# Data Engineer Intern Challenge Question
"""
    Extra Information: You can, if you wish, use frameworks, libraries and external dependencies to help you get faster to the parts you are interested in building,
                       if this helps you; or start from scratch. When building, consider how more features could be added in the future. 

                       Please focus on what interests you the most. If you need inspiration, here are examples of what you can work on. IF you work on these ideas, 
                       we recommend choosing only one or two.

    Ideas:
        SEARCH function
            from characteristics of the images
            from text
            from an image (search for similar images)
        ADD image(s) to the repository
            one / bulk / enormous amount of images
            private or public (permissions)
            secure uploading and stored images
        DELETE image(s)
            one / bulk / selected / all images
            Prevent a user deleting images from another user (access control)
            secure deletion of images
        SELL/BUY images
            ability to manage inventory
            set price
            discounts
            handle money
"""

########################

import logging
from flask import current_app, flash, Flask, Markup, redirect, render_template, make_response
from flask import request, url_for
from flask import send_from_directory

from front import front_page
from form import form_page
import os

from app import app
from dei_db import upload_image_file, get_random_images, get_image_tags

@app.route('/dei')
def dei_list():
    images = get_random_images()
    images = get_image_tags(images)
    print("get_random_images:", images)
    return front_page("dei_list",items=images)

@app.route('/dei/add', methods=['GET', 'POST'])
def dei_add():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        print("data:", data)

        # If an image was uploaded, update the data to point to the new image.
        upload_image_file(request.files.get('image'),data['name'],data['tags'],data['access'])

    return front_page("dei_addsingle","")

@app.route('/dei/addmore', methods=['GET', 'POST'])
def dei_addmore():
    return front_page("dei_addmore","")

@app.route('/dei/uploadimages', methods=['POST'])
def dei_upload_images():
    data = request.form.to_dict(flat=True)

    print("request.files:", request.files)
    files =  request.files.getlist("files[]")
    print("files:", request.files)
    for file in files:
        print("file:", file)
        upload_image_file(file,data['name'],data['tags'],data['access'])
    
    response = make_response("OK", 200)
    return response

@app.route('/dei/image/<imageid>/<ext>', methods=['GET'])
def dei_image(imageid,ext):
    def read_image():
        f = open("F:\\tempimages\\image."+imageid+"."+ext, "rb")
        return  f.read()

    response = make_response(read_image(), 200)
    response.mimetype = "image/"+ext
    return response


@app.route('/dei/search', methods=['GET', 'POST'])
def dei_edit():
    return front_page("dei_search","")

@app.route('/dei/delete', methods=['GET', 'POST'])
def dei_delete():
    return front_page("dei","")
