from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import os
from engineio.payload import Payload
from dotenv import load_dotenv


load_dotenv()


app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

Payload.max_decode_packets = 500
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins


def get_db_connection():
    try:
        connection = pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        db=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT")),
        ssl={'ssl': {'ssl-mode': os.getenv('DB_SSL_MODE')}}
        )
        return connection
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return jsonify({"message": f"Exception occurred: {str(e)}", "exception": str(e)})