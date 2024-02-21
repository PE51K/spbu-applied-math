<!doctype html>
<meta charset="UTF-8">
<html>
<head>
<link href="our-style.css" rel="stylesheet"
type="text/css" />
</head>
<style>
</style>
<body>
<div id="header"><h1></h1></div>
<div id="example">Пример 2.1</div>
<div id="content"><p class="center">Это запись той информации, которую вы
отправили:</p>
<p>
<span>Имя:</span> <b><?php echo $first_name;
?></b><br />
Фамилия: <b><?php echo $last_name;; ?></b><br />
Вас зовут: <b><?php echo $first_name . " " . $last_name;
?></b><br />
Адрес электронной почты: <b><?php echo $_REQUEST['email'];
?></b><br />
URL-адрес Facebook: <b><?php echo $_REQUEST['facebook_url'];
?></b><br />
Идентификатор в Twitter: <b><?php echo
$_REQUEST['twitter_handle']; ?></b><br />
</p>
</div>
<div id="footer"></div>
</body>
</html>
