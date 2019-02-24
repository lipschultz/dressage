import random
from pathlib import Path

from flask import Blueprint, render_template, request, current_app, jsonify
import numpy as np

from dressage.db import get_db

bp = Blueprint('dressage', __name__)

IMG_EXTENSIONS = ('.gif', '.png', '.jpg', '.jpeg', '.jpe', '.bmp')
VIDEO_EXTENSIONS = ('.mp4', '.mpeg4', '.mpeg', '.webm')


@bp.route('/')
def index():
    data = {'refresh-rate': 7 * 60}

    db = get_db()
    cursor = db.execute('SELECT file_reference, rating FROM ratings')
    ratings_map = {r['file_reference']: r['rating'] for r in cursor}

    image_directory = Path(current_app.config['SOURCE_DIRECTORY'])
    images = [f.relative_to(image_directory) for f in image_directory.rglob('*') if f.suffix.lower() in IMG_EXTENSIONS]
    ratings = [2**ratings_map.get(str(f), 3.5) for f in images]
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
    print(f'saving: {file_reference}, {rating}')

    db = get_db()
    db.execute('INSERT INTO ratings (file_reference, rating) '
               'VALUES (?, ?) '
               'ON CONFLICT(file_reference) '
               'DO UPDATE SET rating=excluded.rating',
               (file_reference, rating)
               )
    db.commit()
    return jsonify(result=True)
