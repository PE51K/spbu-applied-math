<?php
include 'db_connect.php'; // Подключаемся к базе данных

// Обработка запроса на удаление
if (isset($_GET['delete'])) {
    $student_id = $_GET['delete'];

    // Сначала удаляем все связанные оценки
    $delete_assessments = $conn->prepare("DELETE FROM assessments WHERE student_id = ?");
    $delete_assessments->bind_param("i", $student_id);
    $delete_assessments->execute();

    // Теперь удаляем студента
    $delete_stmt = $conn->prepare("DELETE FROM students WHERE student_id = ?");
    $delete_stmt->bind_param("i", $student_id);
    $delete_stmt->execute();
    if ($delete_stmt->affected_rows > 0) {
        echo "<p>Студент успешно удален!</p>";
    } else {
        echo "<p>Не удалось удалить студента: " . $conn->error . "</p>";
    }
    $delete_stmt->close();
}


// Запрос к базе данных для получения списка студентов, сортированных по группе и имени
$result = $conn->query("SELECT student_id, full_name, `group` FROM students ORDER BY `group`, full_name");
if ($result === false) {
    die("Ошибка SQL запроса: " . $conn->error);
}
$current_group = null;
?>

<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Список студентов по группам</title>
    <style>
        body {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            font-family: 'Arial', sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 20px;
            color: #333;
        }
        h1, h2 {
            text-align: center;
            color: #0056b3;
        }
        ul {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            list-style-type: none;
            padding: 0;
            width: 80%;
            margin: auto;
        }
        li {
            width: 500px;
            background-color: #fff;
            border: 1px solid #ddd;
            padding: 8px;
            margin-top: 5px;
            border-radius: 4px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        a {
            color: #007BFF;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        .delete-link {
            color: red;
            float: right;
        }
        .back-button, .add-button {
            display: block;
            width: 200px;
            padding: 10px;
            margin: 20px auto;
            background-color: #28a745;
            color: white;
            text-align: center;
            border-radius: 5px;
            text-decoration: none;
        }
        .back-button:hover, .add-button:hover {
            background-color: #1e6b34;
        }
    </style>
</head>
<body>
    <h1>Список студентов по группам</h1>
    <a href="add_student.php" class="add-button">Добавить нового студента</a>
    <ul>
        <?php while ($row = $result->fetch_assoc()): ?>
            <?php
            if ($current_group !== $row['group']) {
                if ($current_group !== null) {
                    echo "</ul>";
                }
                echo "<h2>Группа: " . htmlspecialchars($row['group']) . "</h2><ul>";
                $current_group = $row['group'];
            }
            ?>
            <li>
                <a href="student_details.php?id=<?= $row['student_id'] ?>" style="text-decoration: none; color: black;">
                    <?= htmlspecialchars($row['full_name']) ?>
                </a>
                <a href="?delete=<?= $row['student_id'] ?>" class="delete-link" onclick="return confirm('Вы уверены, что хотите удалить этого студента?');">Удалить</a>
            </li>
        <?php endwhile; ?>
    </ul>
    <a href="index.php" class="back-button">Вернуться в меню</a>
</body>
</html>
