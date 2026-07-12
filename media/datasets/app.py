from flask import Flask, render_template, request, redirect, url_for, session
from tinydb import TinyDB, Query
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secretkey"
XOR_KEY = "mykey"
# Initialize TinyDB

db = TinyDB("database.json")
students = db.table("students")
messages = db.table("messages")
User = Query()

if not students.search(User.username == "admin"):
    students.insert({
        "username": "admin",
        "password": "admin",
        "contact": "0000000000",
        "address": "admin",
        "role": "admin"
    })

def xor_encrypt(text):
    return "".join(
        chr(ord(c) ^ ord(XOR_KEY[i % len(XOR_KEY)]))
        for i, c in enumerate(text)
    )

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        contact = request.form["contact"]
        address = request.form["address"]
        User = Query()
        if students.search(User.username == username):
            return "Username already exists"
        students.insert({
            "username": username,
            "password": password,
            "contact": contact,
            "address": address,
            "role": "user"
        })
        return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        User = Query()
        user = students.get(User.username == username)
        if user and user["password"] == password:
            session["username"] = username
            session["role"] = user.get("role", "user")
            return redirect(url_for("home"))
        return "Invalid credentials"
    return render_template("login.html")

@app.route("/home")
def home():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("home.html")

@app.route("/send", methods=["GET", "POST"])
def send():
    if "username" not in session:
        return redirect(url_for("login"))

    if session.get("role") == "admin":
        return "Admins cannot send messages"

    if request.method == "POST":
        sender = session["username"]
        receiver = request.form["receiver"]
        encrypted_message = xor_encrypt(request.form["message"])

        messages.insert({
            "sender": sender,
            "receiver": receiver,
            "message": encrypted_message,
            "created_at": datetime.utcnow().isoformat()
        })

        return redirect(url_for("inbox"))

    return render_template("send.html")

@app.route("/inbox")
def inbox():
    if "username" not in session:
        return redirect(url_for("login"))
    if session.get("role") == "admin":
        return redirect(url_for("admin"))
    user = session["username"]
    Msg = Query()
    inbox_messages = messages.search(Msg.receiver == user)
    inbox_messages.sort(key=lambda x: x["created_at"], reverse=True)
    decrypted = [
        (m["sender"], xor_encrypt(m["message"]))
        for m in inbox_messages
    ]
    return render_template("inbox.html", messages=decrypted)

@app.route("/admin")
def admin():
    if "username" not in session:
        return redirect(url_for("login"))
    if session.get("role") != "admin":
        return "Access denied"
    all_msgs = messages.all()
    # Convert dicts → tuples (sender, receiver, encrypted_message)
    formatted = [
        (m["sender"], m["receiver"], xor_encrypt(m["message"]))
        for m in all_msgs
    ]
    return render_template("admin.html", messages=formatted)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True) 