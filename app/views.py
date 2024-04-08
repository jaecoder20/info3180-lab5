"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""
from flask import Flask, make_response, request, jsonify
from app import app
from flask import render_template, request, redirect, url_for, flash, send_from_directory
from app.forms import MovieForm
from .models import Movies
from werkzeug.utils import secure_filename
from app import app, db
import os
from flask_wtf.csrf import generate_csrf

###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


@app.route('/api/v1/movies',methods =["POST"])
def movies():
    form = MovieForm()
    data = {}
    if form.validate_on_submit():
        title=form.title.data,
        description=form.description.data,
        poster=form.poster.data
        poster_name  =  secure_filename(poster.filename)
        poster.save(os.path.join(
            app.config['UPLOAD_FOLDER'], poster_name
            ))
        movie = Movies(
        title=title,
        description=description,
        poster_url=poster_name
        )
        db.session.add(movie)
        db.session.commit()
        data = {
            "message": "Movie Successfully added",
            "title": title[0],
            "poster": poster_name,
            "description": description[0] 
        }
    else:
        data = {
            "errors":[
                {error.split(" - ")[0]:error.split(" - ")[1]} for error in form_errors(form)
                    ]
        }
    return make_response(data,200)

@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
 return jsonify({'csrf_token': generate_csrf()})


@app.route('/api/v1/movies', methods=['GET'])
def add_movies():
    movies = db.session.query(Movies).all()
    data = {
        "movies": [
            {"id":movie.id,
             "title":movie.title,
             "description":movie.description,
             "poster":f"/api/v1/posters/{movie.poster_url}"
             } for movie in movies
        ]
    }
    response  = make_response(data,200)
    return response

@app.route('/api/v1/posters/<filename>')
def get_image(filename):
    return send_from_directory(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER']), filename)


###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404