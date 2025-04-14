from flask import Blueprint, render_template, request, jsonify, send_file, current_app
from werkzeug.utils import secure_filename
import os

from app.forms import MovieForm
from app.models import Movie, db
from flask_wtf.csrf import generate_csrf

# Initialize Blueprint
main = Blueprint('main', __name__)

# Home route
@main.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


# Route to handle movie submission (Exercise 3 & 4)
@main.route('/api/v1/movies', methods=['POST'])
def movies():
    # Manually bind form fields and files
    form = MovieForm(request.form)
    form.poster.data = request.files.get('poster')

    if form.validate():
        title = form.title.data
        description = form.description.data
        poster = form.poster.data

        # Securely save poster file
        filename = secure_filename(poster.filename)
        poster.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        # Save movie record to database
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

    # Return validation errors
    return jsonify({"errors": form_errors(form)}), 400


# Route to fetch all movies (Exercise 5)
@main.route('/api/v1/movies', methods=['GET'])
def get_movies():
    movies = Movie.query.all()
    movie_list = []
    for movie in movies:
        movie_list.append({
            "id": movie.id,
            "title": movie.title,
            "description": movie.description,
            "poster": f"/api/v1/posters/{movie.poster}"
        })
    return jsonify({"movies": movie_list})


# Route to serve uploaded movie posters (Exercise 5)
@main.route('/api/v1/posters/<filename>')
def get_poster(filename):
    return send_file(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))


# CSRF token route for VueJS frontend
@main.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()})


# Optional route to serve static text files
@main.route('/<file_name>.txt')
def send_text_file(file_name):
    file_dot_text = file_name + '.txt'
    return current_app.send_static_file(file_dot_text)


# Disable browser caching (for dev/testing convenience)
@main.after_app_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


# Custom 404 error page
@main.app_errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


# Helper: Flatten form validation errors
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
