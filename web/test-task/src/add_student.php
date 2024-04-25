<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Добавить студента</title>
    <style>
        body {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            font-family: 'Arial', sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 20px;
            color: #333;
        }
        h1 {
            color: #0056b3;
        }
        form {
            width: 100%;
            max-width: 500px;
            padding: 20px;
            background: #fff;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
        }
        input[type="text"], button, .back-button {
            width: 100%;
            padding: 10px;
            margin-top: 10px; /* Отступ для всех элементов формы */
            box-sizing: border-box;
        }
        .back-button {
            max-width: 500px;
            background-color: #28a745;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            display: block; /* Чтобы width: 100% сработало */
            text-align: center;
        }
        .back-button:hover {
            max-width: 500px;
            background-color: #1e6b34;
        }
    </style>
</head>
<body>
    <h1>Добавить студента</h1>
    <form method="post" action="add_student.php">
        <p><label>Полное имя:<input type="text" name="full_name" required></label></p>
        <p><label>Группа:<input type="text" name="group" required></label></p>
        <button type="submit">Добавить</button>
    </form>
    <a href="index.php" class="back-button">Вернуться в меню</a>
</body>
</html>
