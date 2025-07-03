from flask import Flask, render_template, request
import random
import string

app = Flask(__name__)

# Generate password using part of name and random characters
def generate_password(name, length):
    base = name[:3].capitalize()
    remaining = max(length - len(base), 0)
    chars = string.ascii_letters + string.digits + string.punctuation
    random_part = ''.join(random.choice(chars) for _ in range(remaining))
    return base + random_part

# Check password strength
def check_strength(password):
    length = len(password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c in string.punctuation for c in password)

    score = sum([has_upper, has_lower, has_digit, has_symbol])
    if length >= 12 and score == 4:
        return "Strong "
    elif length >= 8 and score >= 3:
        return "Medium "
    else:
        return "Weak "

@app.route('/', methods=['GET', 'POST'])
def index():
    password = ""
    strength = ""
    if request.method == 'POST':
        name = request.form['name']
        try:
            length = int(request.form['length'])
            if name and 4 <= length <= 12:
                password = generate_password(name, length)
                strength = check_strength(password)
            else:
                password = "Length must be between 4 and 12"
        except ValueError:
            password = "Invalid input"
    return render_template('index.html', password=password, strength=strength)

if __name__ == '__main__':
    app.run(debug=True)
