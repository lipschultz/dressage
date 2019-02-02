import random
from pathlib import Path

from flask import (
    Blueprint, Markup, flash, g, redirect, render_template, request, url_for, current_app
)
from werkzeug.exceptions import abort

bp = Blueprint('dressage', __name__)

IMG_EXTENSIONS = ('.gif', '.png', '.jpg', '.jpeg', '.jpe', '.bmp')
VIDEO_EXTENSIONS = ('.mp4', '.mpeg4', '.mpeg', '.webm')


@bp.route('/')
def index():
    image_directory = Path(current_app.config['SOURCE_DIRECTORY'])
    images = [f for f in image_directory.rglob('*') if f.suffix.lower() in IMG_EXTENSIONS + VIDEO_EXTENSIONS]
    image = random.choice(images)
    data = {'source': str(image.relative_to(image_directory)),
            'refresh-rate': 7 * 60,
            'type': 'img' if image.suffix.lower() in IMG_EXTENSIONS else 'video'
            }
    return render_template('slideshow.html', content=data)
