# Student Record Management System

## Project Description
The Student Record Management System is a Python Flask web application used to manage student information easily. It allows users to add, view, search, edit, and delete student records. Student data is stored in a JSON file for persistence.

## Features
- Add new student records
- View all student records
- Search for students
- Edit student details
- Delete student records
- Validate email addresses
- Validate GPA between 0 and 10
- Store data in a JSON file
- Display error and success messages

## Technologies Used
- Python
- Flask
- HTML
- CSS
- JSON

## Project Structure
```text
StudentRecordSystem/
├── app.py
├── students.json
├── README.md
└── templates/
    ├── index.html
    └── edit.html
```

## Requirements
- Python 3
- Flask

## How to Run
1. Open a terminal in the project folder.
2. Install Flask:
   `python -m pip install flask`
3. Run the application:
   `python app.py`
4. Open your browser and visit:
   `http://127.0.0.1:5000`

## Data Storage
Student records are stored in `students.json`. Changes are saved to the file so records remain available after restarting the application.

## Author
Student Developer
