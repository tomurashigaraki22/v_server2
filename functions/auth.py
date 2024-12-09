from flask import request, jsonify
import jwt
import datetime
from extensions.extensions import get_db_connection
from constants.generate import generate_tx_id


def userSignup():
    try:
        SECRET_KEY = "thisismyperfectvictory"
        conn = get_db_connection()
        cur = conn.cursor()
        data = request.get_json()

        username = data['username']
        fullname = data['fullname']
        age = data['age']
        nin = data['nin']
        email = data['email']
        password = data['password']

        # Insert user data into the authentication table
        cur.execute("""
            INSERT INTO authentication (username, fullname, age, nin, email, password, status)
            VALUES (%s, %s, %s, %s, %s, %s, 'active')
        """, (username, fullname, age, nin, email, password))

        conn.commit()

        # Generate JWT token
        payload = {
            'username': username,
            'email': email,
            'fullname': fullname,
            'status': "active"
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        cur.close()
        conn.close()

        return jsonify({
            "message": "User registered successfully!",
            "token": token
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400


def userLogin():
    try:
        SECRET_KEY = "thisismyperfectvictory"
        conn = get_db_connection()
        cur = conn.cursor()
        data = request.get_json()

        login_query = data.get('username') or data.get('email')
        password = data.get('password')

        # Check if the user exists by either username or email
        cur.execute("""
            SELECT id, username, fullname, email, password, status FROM authentication
            WHERE username = %s OR email = %s
        """, (login_query, login_query))

        user = cur.fetchone()

        if user:
            # Check if the password is correct
            if user[4] == password:  # user[4] is the password from the query result
                # Generate JWT token
                payload = {
                    'username': user[1],  # username
                    'email': user[3],  # email
                    'fullname': user[2],  # fullname
                    'status': user[5],  # status
                }
                token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

                cur.close()
                conn.close()

                return jsonify({
                    "message": "Login successful!",
                    "token": token,
                    "username": user[1],
                    'fullname': user[2],
                    'email': user[3],
                    "status": user[5]
                }), 200
            else:
                cur.close()
                conn.close()
                return jsonify({"error": "Invalid password"}), 401
        else:
            cur.close()
            conn.close()
            return jsonify({"error": "User not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 400
    


def initializeBalance():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        data = request.get_json()

        username = data['username']
        email = data['email']
        tx_id = generate_tx_id(username)  # Generate tx_id based on the username

        # Check if the record already exists
        cur.execute("""
            SELECT * FROM balance WHERE username = %s OR email = %s
        """, (username, email))
        existing_record = cur.fetchone()

        if existing_record:
            return jsonify({"message": "Balance already initialized for this username or email."}), 400

        # Insert the new balance record
        cur.execute("""
            INSERT INTO balance (username, email, tx_id, balance)
            VALUES (%s, %s, %s, %s)
        """, (username, email, tx_id, 0.00))  # Default balance is 0.00

        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Balance initialized successfully!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400



def fetchBalance():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        data = request.get_json()  # Get query parameters from the URL

        # Extract search criteria (tx_id, username, or email)
        tx_id = data.get('tx_id')
        username = data.get('username')
        email = data.get('email')

        if not any([tx_id, username, email]):  # Check if at least one search parameter is provided
            return jsonify({"error": "Please provide tx_id, username, or email."}), 400

        # Build the query based on the provided criteria
        query = "SELECT username, email, balance, tx_id FROM balance WHERE"
        conditions = []

        if tx_id:
            conditions.append(" tx_id = %s")
        if username:
            conditions.append(" username = %s")
        if email:
            conditions.append(" email = %s")

        query += " AND".join(conditions)

        # Execute the query with the provided values
        cur.execute(query, tuple(filter(None, [tx_id, username, email])))  # Filter out None values
        result = cur.fetchone()

        if result:
            cur.close()
            conn.close()
            # Return the balance details
            return jsonify({
                "username": result[0],
                "email": result[1],
                "balance": result[2],
                "tx_id": result[3]
            }), 200
        else:
            cur.close()
            conn.close()
            return jsonify({"error": "No balance found for the given criteria."}), 404
            

    except Exception as e:
        return jsonify({"error": str(e)}), 400