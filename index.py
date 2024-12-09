from flask import Flask, jsonify, request
from extensions.extensions import get_db_connection, app
from extensions.dbschemas import create_tables
from functions.auth import userLogin, userSignup, initializeBalance, fetchBalance
import requests
from dotenv import load_dotenv
import os

secret_key = os.getenv("SECRET_TEST_KEY")



@app.route("/login", methods=["GET", "POST"])
def loginNow():
    try:
        return userLogin()
    except Exception as e:
        return jsonify({'message': f"Exception occurred: {str(e)}", "exception": str(e)})
    
@app.route("/signup", methods=["GET", "POST"])
def signupNow():
    try:
        return userSignup()
    except Exception as e:
        return jsonify({'message': f"Exception occurred: {str(e)}", "exception": str(e)})
    
@app.route("/init_balance", methods=["GET", "POST"])
def initBalance():
    try:
        return initializeBalance()
    except Exception as e:
        return jsonify({'message': f"Exception occurred: {str(e)}", "exception": str(e)})

@app.route("/fetch_balance", methods=["GET", "POST"])
def fetchBalances():
    try:
        return fetchBalance()
    except Exception as e:
        return jsonify({'message': f"Exception occurred: {str(e)}", "exception": str(e)})
    
@app.route("/get_data_deets", methods=["GET", "POST"])
def getDataShit():
    try:
        # API endpoint for mobile data billers
        url = "https://api.flutterwave.com/v3/bills/MOBILEDATA/billers?country=NG"

        # Flutterwave secret key (Replace with your actual key)
        secret_key = "FLWSECK_TEST-00889be26ada15d9cc0df51ac087dfb1-X"

        # Headers with authorization
        headers = {
            "Authorization": f"Bearer {secret_key}",
            "Content-Type": "application/json",
        }

        # Send GET request to the API
        response = requests.get(url, headers=headers)

        # Parse the response
        if response.status_code == 200:
            data = response.json()
            return jsonify({
                "success": True,
                "data": data
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "Failed to fetch mobile data billers",
                "error": response.json()
            }), response.status_code
    except Exception as e:
        return jsonify({
            "success": False,
            "message": "An error occurred",
            "error": str(e)
        }), 500



if __name__ == "__main__":
    try:
        # Initialize database schemas
        create_tables()
        print("Database schemas initialized successfully.")
    except Exception as e:
        print(f"Exception occurred when initializing database schemas: {str(e)}")

    try:
        # Run SocketIO server
        app.run(host='0.0.0.0', port=1234, debug=True, use_reloader=True)
    except Exception as e:
        print(f"Exception occurred when starting the flask server: {str(e)}")