import random
from pathlib import Path

from flask import Blueprint, render_template, request, current_app, jsonify

from dressage.db import get_db

bp = Blueprint('dressage', __name__)

IMG_EXTENSIONS = ('.gif', '.png', '.jpg', '.jpeg', '.jpe', '.bmp')
VIDEO_EXTENSIONS = ('.mp4', '.mpeg4', '.mpeg', '.webm')


@bp.route('/')
def index():
    data = {'refresh-rate': 7 * 60}

    image_directory = Path(current_app.config['SOURCE_DIRECTORY'])
    images = [f for f in image_directory.rglob('*') if f.suffix.lower() in IMG_EXTENSIONS]
    image = random.choice(images)
    data.update({
        'source': str(image.relative_to(image_directory)),
        'type': 'img' if image.suffix.lower() in IMG_EXTENSIONS else 'video'
    })

    db = get_db()
    row = db.execute('SELECT rating FROM ratings WHERE file_reference = ?', (data['source'], )).fetchone()
    data['rating'] = row['rating'] if row else 0

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
