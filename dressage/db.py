import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'],
                               detect_types=sqlite3.PARSE_DECLTYPES
                               )
        g.db.row_factory = sqlite3.Row

    return g.db


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def record_rating(file_reference, rating):
    db = get_db()
    try:
        db.execute('INSERT INTO ratings (file_reference, rating) '
                   'VALUES (?, ?) '
                   'ON CONFLICT(file_reference) '
                   'DO UPDATE SET rating=excluded.rating',
                   (file_reference, rating)
                   )
        current_app.logger.info('Successfully recorded rating for {file_reference}', file_reference=file_reference)
    except sqlite3.OperationalError as op_err:
        current_app.logger.warn('Encountered OperationalError while recording rating for {file_reference}: {err}', file_reference=file_reference, err=str(op_err))
        try:
            db.execute('INSERT INTO ratings (file_reference, rating) '
                       'VALUES (?, ?)',
                       (file_reference, rating)
                       )
            current_app.logger.info('Successfully recorded rating for {file_reference} after encountering OperationalError', file_reference=file_reference)
        except sqlite3.IntegrityError as int_err:
            current_app.logger.warn('Encountered IntegrityError while recording rating for {file_reference}: {err}', file_reference=file_reference, err=str(int_err))
            db.execute('UPDATE ratings SET rating=? WHERE file_reference=?',
                       (rating, file_reference)
                       )
            current_app.logger.info('Successfully recorded rating for {file_reference} after encountering IntegrityError', file_reference=file_reference)
    db.commit()
    return True
