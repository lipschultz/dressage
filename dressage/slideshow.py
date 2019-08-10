import sqlite3
from pathlib import Path

import numpy as np
from flask import Blueprint, render_template, request, current_app, jsonify

from dressage.db import get_db, record_rating

bp = Blueprint('dressage', __name__)

IMG_EXTENSIONS = ('.gif', '.png', '.jpg', '.jpeg', '.jpe', '.bmp')
VIDEO_EXTENSIONS = ('.mp4', '.mpeg4', '.mpeg', '.webm')


def filename_to_probability(filename, ratings_map):
    rating = ratings_map.get(str(filename), 3.5)
    return 0 if rating == 1 else 2**rating


@bp.route('/')
def index():
    data = {'refresh-rate': 7 * 60}

    db = get_db()
    cursor = db.execute('SELECT file_reference, rating FROM ratings')
    ratings_map = {r['file_reference']: r['rating'] for r in cursor}

    image_directory = Path(current_app.config['SOURCE_DIRECTORY'])
    images = [f.relative_to(image_directory) for f in image_directory.rglob('*') if f.suffix.lower() in IMG_EXTENSIONS]
    ratings = [filename_to_probability(f, ratings_map) for f in images]
    total_rating = sum(ratings)
    ratings_distr = [r / total_rating for r in ratings]

    image = np.random.choice(images, p=ratings_distr)
    data.update({
        'source': str(image),
        'type': 'img' if image.suffix.lower() in IMG_EXTENSIONS else 'video',
        'rating': ratings_map.get(str(image), 0)
    })

    return render_template('slideshow.html', content=data)


@bp.route('/_save_rating')
def save_rating():
    file_reference = request.args.get('file_reference')
    rating = request.args.get('rating')
    print('saving: {file_reference}, {rating}'.format(file_reference=file_reference, rating=rating))

    result = record_rating(file_reference, rating)
    return jsonify(result=result)


@bp.route('/_flag_picture')
def flag_picture():
    file_reference = request.args.get('file_reference')
    with open(current_app.config['FLAG_FILE'], 'a') as fp:
        fp.write('{file_reference}\n'.format(file_reference=file_reference))
    return jsonify(result=True)
