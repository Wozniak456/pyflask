import os
from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='VERY_SECRET_KEY',
        DATABASE=os.path.join(app.instance_path, 'db.sqlite'),
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #for new functionality

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import records
    app.register_blueprint(records.bp)
    app.add_url_rule('/', endpoint='index')

    from . import categories
    app.register_blueprint(categories.bp)
    app.add_url_rule('/', endpoint='index')

    return app