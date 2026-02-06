import sqlite3
from flask import Flask, request, abort

app = Flask(__name__)

# FIX 1: Move secrets to Environment Variables (Simulation)
# In production, use AWS Secrets Manager or HashiCorp Vault.
import os
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD") 

@app.route("/user-search")
def search():
    username = request.args.get('name')
    
    # FIX 2: Parameterized Query (Prevents SQL Injection)
    # The '?' acts as a placeholder; the DB driver handles escaping.
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (username,)) # Data is passed as a separate tuple
    
    # FIX 3: Safe Command Handling (Prevents Command Injection)
    # Never use eval(). Use a "whitelist" of allowed commands.
    allowed_commands = {
        "status": "System is healthy",
        "version": "v1.0.4"
    }
    cmd = request.args.get('debug_cmd')
    response = allowed_commands.get(cmd, "Invalid Command")
    
    return f"Search complete: {response}"

if __name__ == "__main__":
    app.run(debug=False) # FIX 4: Disable Debug mode in production