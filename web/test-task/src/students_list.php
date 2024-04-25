<?php
include 'db_connect.php'; // Подключаемся к базе данных

// Обработка запроса на удаление
if (isset($_GET['delete'])) {
    $student_id = $_GET['delete'];
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
</head>
<body>
    <h1>Список студентов по группам</h1>
    <a href="add_student.php">Добавить нового студента</a>
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
                    <?= htmlspecialchars($row['full_name']) ?> (Группа: <?= htmlspecialchars($row['group']) ?>)
                </a>
                - <a href="?delete=<?= $row['student_id'] ?>" onclick="return confirm('Вы уверены, что хотите удалить этого студента?');" style="color: red;">Удалить</a>
            </li>
        <?php endwhile; ?>
    </ul>
    <a href="index.php" style="display: inline-block; margin-top: 20px; padding: 8px 16px; background-color: #28a745; color: white; text-decoration: none; border-radius: 5px;">Вернуться в меню</a>
</body>
</html>
