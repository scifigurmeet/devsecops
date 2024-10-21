from flask import Flask, request, render_template_string
import re

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Secure Flask App</title>
</head>
<body>
    <h1>Welcome to Secure Flask App</h1>
    <form method="POST">
        <input type="text" name="user_input" placeholder="Enter your name">
        <input type="submit" value="Submit">
    </form>
    {% if name %}
    <h2>Hello, {{ name }}!</h2>
    {% endif %}
</body>
</html>
"""

@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

@app.route('/', methods=['GET', 'POST'])
def hello():
    name = None
    if request.method == 'POST':
        user_input = request.form.get('user_input', '')
        if re.match("^[A-Za-z0-9 ]+$", user_input):
            name = user_input
        else:
            name = "Invalid input"
    return render_template_string(HTML_TEMPLATE, name=name)

if __name__ == '__main__':
    app.run(debug=True)
