<?php
include 'db_connect.php'; // Подключение к базе данных

$student_id = $_GET['id'] ?? 0; // Получаем ID студента из URL
$student_id = intval($student_id); // Преобразуем в целое число для безопасности

// Получение данных студента
$student_query = $conn->prepare("SELECT full_name, `group` FROM students WHERE student_id = ?");
$student_query->bind_param("i", $student_id);
$student_query->execute();
$student_result = $student_query->get_result();
$student = $student_result->fetch_assoc();

// Получение оценок студента
$assessments_query = $conn->prepare("SELECT a.assessment_id, s.name as subject_name, a.type, a.passed, a.grade FROM assessments a JOIN subjects s ON a.subject_id = s.subject_id WHERE a.student_id = ?");
$assessments_query->bind_param("i", $student_id);
$assessments_query->execute();
$assessments = $assessments_query->get_result();

// Обработка POST запроса для обновления оценок
if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST['update_grades'])) {
    foreach ($_POST['assessments'] as $assessment_id => $assessment_data) {
        $update_query = $conn->prepare("UPDATE assessments SET passed = ?, grade = ? WHERE assessment_id = ?");
        $passed = $assessment_data['passed'] ? 1 : 0;
        $grade = $assessment_data['grade'];
        $update_query->bind_param("isi", $passed, $grade, $assessment_id);
        $update_query->execute();
    }
    echo "<p>Оценки обновлены!</p>";
}

$student_query->close();
$assessments_query->close();
?>

<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Детали студента</title>
</head>
<body>
    <h1>Детали студента: <?= htmlspecialchars($student['full_name']) ?></h1>
    <h2>Группа: <?= htmlspecialchars($student['group']) ?></h2>
    <form method="post">
        <?php while ($row = $assessments->fetch_assoc()): ?>
        <div>
            <label><?= htmlspecialchars($row['subject_name']) ?> - <?= htmlspecialchars($row['type']) ?></label>
            <select name="assessments[<?= $row['assessment_id'] ?>][passed]">
                <option value="0" <?= !$row['passed'] ? 'selected' : '' ?>>Не сдан</option>
                <option value="1" <?= $row['passed'] ? 'selected' : '' ?>>Сдан</option>
            </select>
            <input type="text" name="assessments[<?= $row['assessment_id'] ?>][grade]" value="<?= htmlspecialchars($row['grade']) ?>">
        </div>
        <?php endwhile; ?>
        <button type="submit" name="update_grades">Обновить оценки</button>
    </form>
    <a href="students_list.php">Вернуться к списку студентов</a>
</body>
</html>
