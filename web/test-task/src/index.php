<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Система учета оценок студентов</title>
    <style>
        body {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            font-family: 'Arial', sans-serif; /* Используем шрифт Arial для тела документа */
            background-color: #f4f4f4; /* Светло-серый фон для страницы */
            margin: 0;
            padding: 20px;
            color: #333; /* Темно-серый текст */
        }
        h1 {
            color: #0056b3; /* Синий цвет для заголовков */
            text-align: center;
        }
        ul {
            list-style-type: none; /* Убираем маркеры списка */
            padding: 0;
        }
        li {
            text-align: center;
            max-width: 500px;
            background-color: #ffffff; /* Белый фон для элементов списка */
            border: 1px solid #ddd; /* Граница вокруг элементов */
            margin-top: 8px; /* Отступ сверху для элементов */
            padding: 10px 20px; /* Поля вокруг текста */
            border-radius: 5px; /* Скругленные углы */
            box-shadow: 0 2px 5px rgba(0,0,0,0.1); /* Тень под элементами */
        }
        a {
            text-align: center;
            max-width: 500px;
            color: #0056b3; /* Синий цвет ссылок */
            text-decoration: none; /* Убираем подчеркивание текста */
            font-weight: bold; /* Жирный шрифт для текста */
        }
        a:hover {
            text-align: center;
            max-width: 500px;
            text-decoration: underline; /* Подчеркивание при наведении */
        }
    </style>
</head>
<body>
    <h1>Добро пожаловать в систему учета оценок студентов</h1>
    <ul>
        <li><a href="add_student.php">Добавить студента</a></li>
        <li><a href="students_list.php">Список студентов по группам</a></li>
    </ul>
</body>
</html>
