import sqlite3
from flask import Flask, request

app = Flask(__name__)

# VULNERABILITY 1: Hardcoded Secret (SAST will catch this)
ADMIN_PASSWORD = "SuperSecretPassword123!" 

@app.route("/user-search")
def search():
    username = request.args.get('name')
    
    # VULNERABILITY 2: SQL Injection (Source-to-Sink Taint)
    # The 'username' comes directly from the user and is concatenated into the query.
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = '%s'" % username
    cursor.execute(query)
    
    # VULNERABILITY 3: Command Injection / Dangerous Eval
    # Taking user input and passing it to a dangerous sink.
    eval(request.args.get('debug_cmd')) 
    
    return "Search complete"

if __name__ == "__main__":
    app.run(debug=True)