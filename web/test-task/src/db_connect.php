<?php
$servername = "db"; // Имя хоста базы данных, `db` в случае использования docker-compose
$username = "user"; // Имя пользователя для базы данных
$password = "password"; // Пароль для базы данных
$database = "student_grades"; // Название базы данных

// Создание подключения
$conn = new mysqli($servername, $username, $password, $database);

// Проверка подключения
if ($conn->connect_error) {
    die("Ошибка подключения: " . $conn->connect_error);
}
?>
