''' controller and routes for upload '''
import os
import pathlib
from flask import request, jsonify
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)
from app import app, mongo, flask_bcrypt, jwt
from app.schemas import validate_user
import logger
import json


# @app.route('/result-lstm_model', methods = ['GET', 'POST'])
# @jwt_required
# def start():

#   return jsonify({'ok': True, 'session_id': session_id}), 200