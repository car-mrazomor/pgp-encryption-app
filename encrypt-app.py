from flask import Flask, jsonify, request, send_file

import os

from datetime import datetime
from flask import Flask, request, render_template, url_for, send_file, redirect, jsonify
from flask_cors import CORS, cross_origin
from flask import send_from_directory
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
from flask_login import LoginManager
from flask_login import login_user
from flask_login import login_required, current_user, logout_user
from flask_login import UserMixin
import os

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import IntegerField, StringField, SubmitField, FileField
from wtforms.validators import DataRequired

import threading
import os
import requests
import imaplib

import random

from datetime import datetime

from encrypt import get_private_public_key, generate_user_key_pair
from encrypt import decrypt_b64, decrypt_data
from encrypt import encrypt_data, encrypt_b64

app = Flask(__name__)
cors = CORS(app)
app.url_map.strict_slashes = False
app.config['SECRET_KEY'] = 'MGmEHBdhPXi7dKoP5VUViR-jn0cKwpTalniD.ZipEytlOJh9APHVLjibesp-nQ7md0QRsfXidvh'
bootstrap = Bootstrap(app)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/api/generateKeys", methods=["GET"])
def generate_keys():
    try:
        public_pem, private_pem = generate_user_key_pair()
    except Exception as e:
        return jsonify({"status":"failed", "message":"error"})
    return jsonify({"status":"ok", "message":"Keys are generated", "public_pem":public_pem.decode(), "private_pem":private_pem.decode()})

@app.route("/api/encryptData/", methods=["POST"])
def encryptData():
    data = request.form
    plain_text = data.get("plain_text")
    public_pem = data.get("public_pem")
    try:
        public_key = get_private_public_key(public_pem=public_pem.encode())
    except Exception as e:
        return jsonify({"status":"failed", "message":"error"})
    try:
        encrypted_data = encrypt_data(plain_text, public_key)
    except Exception as e:
        return jsonify({"status":"failed", "message":"error"})
    return jsonify({"status":"ok", "message":"Data encrypted", "encryptedData":encrypted_data})

@app.route("/api/decryptData/", methods=["POST"])
def decryptData():
    data = request.form
    encrypted_data = data.get("encrypted_data")
    private_pem = data.get("private_pem")
    try:
        private_key = get_private_public_key(private_pem=private_pem.encode())
    except:
        return jsonify({"status":"failed", "message":"error"})
    try:
        plain_text = decrypt_data(encrypted_data, private_key)
    except Exception as e:
        return jsonify({"status":"failed", "message":"error"})
    return jsonify({"status":"ok", "message":"Data decrypted", "decryptedData":plain_text})

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/logo_icon.png')
def logo_icon_light():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'logo_icon.png', mimetype='image/png')

@app.route('/tables.txt')
def robots():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'tables.txt')

@app.errorhandler(404)
def page_not_found(e):
    return {"error":"404 | page not found."}

app.run(host="0.0.0.0", port=5050)