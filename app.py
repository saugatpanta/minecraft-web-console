from flask import Flask, render_template, redirect, url_for
import mysql.connector
import subprocess
import os

# Initialize the Flask application
app = Flask(__name__)

# MySQL connection setup
def get_db_connection():
    connection = mysql.connector.connect(
        host="127.0.0.1",  # MySQL server address
        user="root",       # MySQL username
        password="saugat@9767582302",  # MySQL password
        database="minecraft_dashboard"  # Database name
    )
    return connection

# Route to display the server status and console
@app.route('/')
def index():
    connection = get_db_connection()
    cursor = connection.cursor()

    # Fetch current server status
    cursor.execute("SELECT status FROM server_state WHERE id = 1")
    result = cursor.fetchone()
    status = result[0]

    connection.close()
    
    return render_template('index.html', status=status)

# Route to start the Minecraft server
@app.route('/start', methods=['POST'])
def start_server():
    # Start the server using subprocess (assuming the server is started by a command line)
    try:
        subprocess.Popen(['java', '-Xmx1024M', '-Xms1024M', '-jar', 'server.jar', 'nogui'])
        
        # Update the status in the database
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("UPDATE server_state SET status = 'started' WHERE id = 1")
        connection.commit()
        connection.close()
        
    except Exception as e:
        print(f"Error starting server: {e}")
    
    return redirect(url_for('index'))

# Route to stop the Minecraft server
@app.route('/stop', methods=['POST'])
def stop_server():
    try:
        # Stop the Minecraft server (You can adapt this based on your server setup)
        os.system("taskkill /F /IM java.exe")

        # Update the status in the database
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("UPDATE server_state SET status = 'stopped' WHERE id = 1")
        connection.commit()
        connection.close()
        
    except Exception as e:
        print(f"Error stopping server: {e}")
    
    return redirect(url_for('index'))

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
