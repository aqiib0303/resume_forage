from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

auth_bp = Blueprint("auth", __name__)

# --- Database Helper ---
def get_db():
    conn = sqlite3.connect("instance/users.db")
    conn.row_factory = sqlite3.Row
    return conn

# --- Signup ---
@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()
        cur = conn.cursor()

        # check if user exists
        cur.execute("SELECT * FROM users WHERE email=?", (email,))
        if cur.fetchone():
            flash("Email already registered!", "error")
            return redirect(url_for("auth.signup"))

        hashed_pw = generate_password_hash(password)
        cur.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                    (name, email, hashed_pw))
        conn.commit()
        conn.close()
        flash("Signup successful! Please login.", "success")
        return redirect(url_for("auth.login"))
    return render_template("signup.html")

# --- Login ---
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cur.fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            flash("Welcome back, " + user["name"], "success")
            return redirect(url_for("resume.builder"))
        else:
            flash("Invalid credentials", "error")

    return render_template("login.html")

# --- Logout ---
@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))


@auth_bp.route("/blog")
def blog():
    """Show blog page with articles and template-related content."""
    return render_template("blog.html")


# 📌 Contact Route
@auth_bp.route("/contact")
def contact():
    """Show contact page with WhatsApp link and developer info."""
    return render_template("contact.html")
