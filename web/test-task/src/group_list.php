<?php
include 'db_connect.php'; // Подключаемся к базе данных

// Удаление студента
if (isset($_GET['delete'])) {
    $student_id = $_GET['delete'];
    $delete_stmt = $conn->prepare("DELETE FROM students WHERE student_id = ?");
    $delete_stmt->bind_param("i", $student_id);
    $delete_stmt->execute();
    if ($delete_stmt->affected_rows > 0) {
        echo "Студент успешно удален!";
    } else {
        echo "Не удалось удалить студента: " . $conn->error;
    }
    $delete_stmt->close();
}

// Получаем список студентов
$result = $conn->query("SELECT student_id, full_name, group FROM students");
?>

<!DOCTYPE html>
<html>
<head>
    <title>Список студентов</title>
</head>
<body>
    <h1>Список студентов</h1>
    <ul>
        <?php while ($row = $result->fetch_assoc()): ?>
            <li>
                <?= htmlspecialchars($row['full_name']) ?> - <?= htmlspecialchars($row['group']) ?>
                <a href="?delete=<?= $row['student_id'] ?>">Удалить</a>
            </li>
        <?php endwhile; ?>
    </ul>
</body>
</html>
