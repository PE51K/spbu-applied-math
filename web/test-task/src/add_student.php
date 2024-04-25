<?php
// Подключение к базе данных
include 'db_connect.php';

// Обработка POST запроса
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $full_name = $_POST['full_name'];
    $group = $_POST['group'];

    // Подготовка и выполнение запроса к базе данных
    $stmt = $conn->prepare("INSERT INTO students (full_name, `group`) VALUES (?, ?)");
    if ($stmt === false) {
        die("Ошибка при подготовке запроса: " . $conn->error);
    }

    $stmt->bind_param("ss", $full_name, $group);
    $result = $stmt->execute();

    if ($result) {
        echo "Студент успешно добавлен!";
    } else {
        echo "Ошибка при добавлении студента: " . $stmt->error;
    }
    $stmt->close();
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Добавить студента</title>
</head>
<body>
    <h1>Добавить студента</h1>
    <form method="post" action="add_student.php">
        <p>
            <label>Полное имя:
                <input type="text" name="full_name" required>
            </label>
        </p>
        <p>
            <label>Группа:
                <input type="text" name="group" required>
            </label>
        </p>
        <button type="submit">Добавить</button>
    </form>
    <a href="index.php" style="display: inline-block; margin-bottom: 20px; padding: 8px 16px; background-color: #28a745; color: white; text-decoration: none; border-radius: 5px;">Вернуться в меню</a>
</body>
</html>
