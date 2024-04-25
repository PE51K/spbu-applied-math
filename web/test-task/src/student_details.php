<?php
include 'db_connect.php'; // Подключение к базе данных

$student_id = $_GET['id'] ?? 0; // Получаем ID студента из URL
$student_id = intval($student_id); // Преобразуем в целое число для безопасности

// Обработка POST запроса для обновления или добавления оценок
if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST['update_grades'])) {
    foreach ($_POST['assessments'] as $subject_id => $assessment_data) {
        // Проверяем, существует ли уже оценка
        $check_query = $conn->prepare("SELECT assessment_id FROM assessments WHERE student_id = ? AND subject_id = ?");
        $check_query->bind_param("ii", $student_id, $subject_id);
        $check_query->execute();
        $existing = $check_query->get_result()->fetch_assoc();

        if ($existing) {
            // Обновляем существующую запись
            $update_query = $conn->prepare("UPDATE assessments SET type = ?, passed = ?, grade = ? WHERE assessment_id = ?");
            $update_query->bind_param("sisi", $assessment_data['type'], $assessment_data['passed'], $assessment_data['grade'], $existing['assessment_id']);
        } else {
            // Добавляем новую запись
            $update_query = $conn->prepare("INSERT INTO assessments (student_id, subject_id, type, passed, grade) VALUES (?, ?, ?, ?, ?)");
            $update_query->bind_param("iisis", $student_id, $subject_id, $assessment_data['type'], $assessment_data['passed'], $assessment_data['grade']);
        }
        $update_query->execute();
    }
    echo "<p>Оценки обновлены!</p>";
}

// Получение данных студента
$student_query = $conn->prepare("SELECT full_name, `group` FROM students WHERE student_id = ?");
$student_query->bind_param("i", $student_id);
$student_query->execute();
$student_result = $student_query->get_result();
$student = $student_result->fetch_assoc();

// Получение списка всех предметов и оценок студента по этим предметам после возможного обновления
$subjects_query = $conn->query("SELECT s.subject_id, s.name AS subject_name, a.type, a.passed, a.grade FROM subjects s LEFT JOIN assessments a ON s.subject_id = a.subject_id AND a.student_id = $student_id");

$student_query->close();
?>

<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Детали студента</title>
    <style>
        body {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            font-family: 'Arial', sans-serif;
            background-color: #f4f4f4;
            color: #333;
            padding: 20px;
            margin: 0;
        }
        h1, h2 {
            text-align: center;
            color: #0056b3;
        }
        form {
            max-width: 500px;
            margin: auto;
            padding: 20px;
            background: #fff;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        label {
            font-weight: bold;
            margin-top: 10px;
        }
        select {
            width: 100%;
            padding: 8px;
            margin-top: 5px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        button {
            width: 100%;
            padding: 10px;
            background-color: #007BFF;
            color: white;
            border: none;
            border-radius: 4px;
            margin-top: 20px;
            cursor: pointer;
        }
        button:hover {
            background-color: #0056b3;
        }
        .back-button {
            display: inline-block;
            width: 200px;
            padding: 10px;
            background-color: #28a745;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            text-align: center;
            margin-top: 20px;
        }
        .back-button:hover {
            background-color: #1e6b34;
        }
    </style>
</head>
<body>
    <h1>Детали студента: <?= htmlspecialchars($student['full_name']) ?></h1>
    <h2>Группа: <?= htmlspecialchars($student['group']) ?></h2>
    <form method="post">
        <?php while ($row = $subjects_query->fetch_assoc()): ?>
        <div>
            <label><?= htmlspecialchars($row['subject_name']) ?></label>
            <select name="assessments[<?= $row['subject_id'] ?>][passed]">
                <option value="0" <?= !$row['passed'] ? 'selected' : '' ?>>Не сдан</option>
                <option value="1" <?= $row['passed'] ? 'selected' : '' ?>>Сдан</option>
            </select>
            <select name="assessments[<?= $row['subject_id'] ?>][grade]">
                <option value="" <?= $row['grade'] === '' ? 'selected' : '' ?>>Выберите оценку</option>
                <option value="A" <?= $row['grade'] === 'A' ? 'selected' : '' ?>>A</option>
                <option value="B" <?= $row['grade'] === 'B' ? 'selected' : '' ?>>B</option>
                <option value="C" <?= $row['grade'] === 'C' ? 'selected' : '' ?>>C</option>
                <option value="D" <?= $row['grade'] === 'D' ? 'selected' : '' ?>>D</option>
                <option value="F" <?= $row['grade'] === 'F' ? 'selected' : '' ?>>F</option>
            </select>
        </div>
        <?php endwhile; ?>
        <button type="submit" name="update_grades">Обновить оценки</button>
    </form>
    <a href="students_list.php" class="back-button">Вернуться к списку студентов</a>
</body>
</html>
