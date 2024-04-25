CREATE DATABASE student_grades;

USE student_grades;

CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fullname VARCHAR(255) NOT NULL,
    group_name VARCHAR(50) NOT NULL
);

CREATE TABLE assessments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    subject VARCHAR(100) NOT NULL,
    project_work BOOLEAN,
    test BOOLEAN,
    credit BOOLEAN,
    exam BOOLEAN,
    FOREIGN KEY (student_id) REFERENCES students(id)
);
