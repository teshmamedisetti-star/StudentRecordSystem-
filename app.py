
from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os
import re

app = Flask(__name__)
app.secret_key = "student-record-secret"

DATA_FILE = os.path.join(app.root_path, "students.json")


def load_students():
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_students(students):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(students, file, indent=4)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        student_id = request.form.get("student_id", "").strip()
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        gpa_text = request.form.get("gpa", "").strip()

        if not all([student_id, name, email, gpa_text]):
            flash("Please fill in all fields.")
            return redirect(url_for("home"))

        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            flash("Please enter a valid email address.")
            return redirect(url_for("home"))

        try:
            gpa = float(gpa_text)
            if not 0 <= gpa <= 10:
                raise ValueError
        except ValueError:
            flash("GPA must be between 0 and 10.")
            return redirect(url_for("home"))

        students = load_students()

        if any(s.get("student_id", "").casefold() == student_id.casefold()
               for s in students):
            flash("Student ID already exists.")
            return redirect(url_for("home"))

        students.append({
            "student_id": student_id,
            "name": name,
            "email": email,
            "gpa": gpa
        })

        try:
            save_students(students)
            flash("Student added successfully!")
        except OSError:
            flash("Could not save student record.")

        return redirect(url_for("home"))

    students = load_students()
    search = request.args.get("search", "").strip().casefold()

    if search:
        students = [
            s for s in students
            if search in s.get("student_id", "").casefold()
            or search in s.get("name", "").casefold()
        ]

    return render_template("index.html", students=students, search=search)



@app.route("/delete/<student_id>", methods=["POST"])
def delete_student(student_id):
    students = load_students()

    students = [
        student for student in students
        if student.get("student_id") != student_id
    ]

    save_students(students)
    flash("Student deleted successfully.")
    return redirect(url_for("home"))

@app.route("/edit/<student_id>", methods=["GET", "POST"])
def edit_student(student_id):
    students = load_students()

    student = next(
        (s for s in students if s.get("student_id") == student_id),
        None
    )

    if student is None:
        flash("Student not found.")
        return redirect(url_for("home"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        gpa_text = request.form.get("gpa", "").strip()

        if not name or not email or not gpa_text:
            flash("Please fill in all fields.")
            return render_template("edit.html", student=student)

        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            flash("Please enter a valid email.")
            return render_template("edit.html", student=student)

        try:
            gpa = float(gpa_text)
            if not 0 <= gpa <= 10:
                raise ValueError
        except ValueError:
            flash("GPA must be between 0 and 10.")
            return render_template("edit.html", student=student)

        student["name"] = name
        student["email"] = email
        student["gpa"] = gpa

        save_students(students)
        flash("Student updated successfully!")
        return redirect(url_for("home"))

    return render_template("edit.html", student=student)

  
if __name__ == "__main__":
    app.run(debug=False)