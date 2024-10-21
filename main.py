from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import pymysql

app = Flask(__name__)
socketio = SocketIO(app)

# MySQL connection setup
timeout = 10
conn = pymysql.connect(
    charset="utf8mb4",
    connect_timeout=timeout,
    cursorclass=pymysql.cursors.DictCursor,
    db="defaultdb",
    host="mysql-30059af1-yogyachugh-695c.b.aivencloud.com",
    password="AVNS_C23ljLnWIaThTRYI9YZ",
    read_timeout=timeout,
    port=27336,
    user="avnadmin",
    write_timeout=timeout,
)
cursor = conn.cursor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start-test', methods=['POST'])
def start_test():
    time_allotted = request.json.get('time', 60)  # Default to 60 seconds if not provided
    socketio.emit('start_test', {
        'message': 'Test is starting',
        'time': time_allotted
    })
    return jsonify({'status': 'success'})

@app.route('/submit-results', methods=['POST'])
def submit_results():
    # Store complete files (results) in MySQL database
    data = request.json
    user_name = data['username']  # Get username
    file_contents = data['file_contents']  # List of file contents from the client
    print(user_name,"\n",file_contents)

    try:
        # Create a single entry for the user with three files
        query = "INSERT INTO test_results (username, file1, file2, file3) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (user_name, file_contents[0], file_contents[1], file_contents[2]))
        conn.commit()
    except Exception as e:
        print(f"Error storing results: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

    return jsonify({'status': 'success'})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
