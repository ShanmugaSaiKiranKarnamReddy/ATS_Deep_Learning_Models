''' controller and routes for extracting corpus '''
import os
import pathlib
from flask import request, jsonify
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required, get_jwt_identity)
from app import app, mongo, flask_bcrypt, jwt
from app.schemas import validate_user
import logger
import json
from werkzeug.utils import secure_filename

@app.route('/extractJdCorpus', methods = ['GET', 'POST'])
@jwt_required
def extractJdCorpus():
  user = get_jwt_identity()
  
  return jsonify({'ok': True, 'data': user}), 200