from flask import Flask, render_template, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='#1e1e1b#6c63ff',
            database='CrudWithFlask'
        )
        return connection
    except Error as e:
        print(f"The error '{e}' occurred")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['POST'])
def create():
    data = request.get_json()
    name = data['name']
    email = data['email']
    password = data['password']

    if not name or not email or not password:
        return jsonify({'message': 'error'})

    connection = create_connection()
    if connection is None:
        return jsonify({'message': 'database connection error'})

    try:
        cursor = connection.cursor()
        query = """
        INSERT INTO users (name, email, password) VALUES (%s, %s, %s)
        """
        cursor.execute(query, (name, email, password))
        connection.commit()
        return jsonify({'message': 'created'})
    except Error as e:
        print(f"The error '{e}' occurred")
        return jsonify({'message': 'error'})
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/read', methods=['GET'])
def read():
    return None

if __name__ == '__main__':
    app.run(debug=True)