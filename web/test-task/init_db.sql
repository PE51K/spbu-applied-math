CREATE DATABASE IF NOT EXISTS student_grades;
USE student_grades;

-- Создание таблиц
CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    `group` VARCHAR(50) NOT NULL  -- Enclosed in backticks
);

CREATE TABLE subjects (
    subject_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE assessments (
    assessment_id INT AUTO_INCREMENT PRIMARY KEY,
    type VARCHAR(50) NOT NULL,
    subject_id INT,
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
);

CREATE TABLE student_assessments (
    student_assessment_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    assessment_id INT,
    status VARCHAR(50),
    grade INT,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (assessment_id) REFERENCES assessments(assessment_id)
);
