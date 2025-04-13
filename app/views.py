from flask import Blueprint, render_template, request, jsonify, send_file, current_app
from werkzeug.utils import secure_filename
import os

from app.forms import MovieForm
from app.models import Movie, db

main = Blueprint('main', __name__)

# Home route
@main.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


# Route to handle movie submission (Exercise 3)
@main.route('/api/v1/movies', methods=['POST'])
def movies():
    form = MovieForm()
    
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        poster = form.poster.data

        # Save the poster file securely
        filename = secure_filename(poster.filename)
        poster.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        # Save to database
        new_movie = Movie(
            title=title,
            description=description,
            poster=filename
        )
        db.session.add(new_movie)
        db.session.commit()

        return jsonify({
            "message": "Movie Successfully added",
            "title": title,
            "poster": filename,
            "description": description
        }), 201

    return jsonify({"errors": form_errors(form)}), 400


# Route to serve static .txt files (optional)
@main.route('/<file_name>.txt')
def send_text_file(file_name):
    file_dot_text = file_name + '.txt'
    return current_app.send_static_file(file_dot_text)


# Disable browser caching (for dev convenience)
@main.after_app_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


# Custom 404 error page
@main.app_errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


# Helper: Collect form validation errors
def form_errors(form):
    error_messages = []
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            )
            error_messages.append(message)
    return error_messages
