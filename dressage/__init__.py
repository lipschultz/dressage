import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SOURCE_DIRECTORY=os.path.join(app.instance_path, '..', 'images'),
        DATABASE=os.path.join(app.instance_path, 'dressage.sqlite'),
        FLAG_FILE=os.path.join(app.instance_path, '..', 'flag.log'),
        # SOURCE_DIRECTORY=os.path.join(app.instance_path, 'static', 'images')
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    from . import slideshow
    app.register_blueprint(slideshow.bp)
    # app.add_url_rule('/', endpoint='index')

    return app
