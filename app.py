
# -*- coding: utf-8 -*-

import os

from flask import Flask, jsonify, make_response
# from flask.ext.cors import CORS

from db import db
from api import api
# import config file
import config


def create_app(config):
    # init our app
    app = Flask(__name__)
    app.secret_key = 'djfjsdkjXXS7979dfdfd'
    # load config values from the config file
    app.config.from_object(config)

    # init sqlalchemy db instance
    db.init_app(app)
    db.app = app

    # register blueprints
    app.register_blueprint(api)

 #   configure_errorhandlers(app)
 #   configure_cors(app)
 #   configure_logging(app)

    # all set; return app object
    return app


if __name__ == "__main__":
    app = create_app(config)
    app.run(debug=True, host='0.0.0.0', threaded=True)
