from flask import Flask, session, redirect, url_for, request, render_template_string
import redis

app = Flask(__name__)
app.secret_key = "supersecretkey"
cache = redis.Redis(host='redis', port=6379)

# Login HTML template
login_page = """
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
</head>
<body style="display:flex; justify-content:center; align-items:center; height:100vh; font-family:sans-serif;">
    <form method="POST">
        <h2>Login</h2>
        <input type="text" name="username" placeholder="Enter username" required />
        <br><br>
        <input type="submit" value="Login"/>
    </form>
</body>
</html>
"""

# Dashboard HTML template with animations
dashboard = """
<!DOCTYPE html>
<html>
<head>
    <title>Welcome</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            text-align: center;
            margin-top: 100px;
            background: #f0f8ff;
            animation: fadeIn 2s ease-in;
        }
        h2 {
            font-size: 2.5em;
            color: #333;
            animation: slideIn 1.5s ease-out;
        }
        p {
            font-size: 1.3em;
            margin-top: 20px;
        }
        a {
            margin-top: 30px;
            display: inline-block;
            text-decoration: none;
            background: #007bff;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            transition: 0.3s;
        }
        a:hover {
            background: #0056b3;
        }
        @keyframes fadeIn {
            from {opacity: 0;}
            to {opacity: 1;}
        }
        @keyframes slideIn {
            from {transform: translateY(-30px); opacity: 0;}
            to {transform: translateY(0); opacity: 1;}
        }
    </style>
</head>
<body>
    <h2>👋 Welcome Buddi Papa, {{ username }} 😄</h2>
    <p>🚀 This page has been visited <strong>{{ visits }}</strong> times.</p>
    <a href="{{ url_for('logout') }}">🚪 Logout</a>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('home'))
    return render_template_string(login_page)

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    visits = cache.incr('visits')
    return render_template_string(dashboard, username=session['username'], visits=visits)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

