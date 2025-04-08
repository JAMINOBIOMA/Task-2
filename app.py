from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Function to establish a database connection
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",      
            user="root",      
            password="Exoteric7465@",  
            database="secure_db" 
        )
        if connection.is_connected():
            print("Connected to MySQL database")
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Route to insert data securely
@app.route('/insert', methods=['POST'])
def insert_data():
    data = request.json.get("data_value")
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "INSERT INTO data_records (data_value) VALUES (%s)"
            cursor.execute(query, (data,))
            connection.commit()
            return jsonify({"message": "Data inserted securely!"})
        except mysql.connector.IntegrityError:
            return jsonify({"error": "Duplicate entry detected!"}), 400
        except Error as e:
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            connection.close()
    else:
        return jsonify({"error": "Database connection failed"}), 500

if __name__ == '__main__':
    app.run(debug=True)
