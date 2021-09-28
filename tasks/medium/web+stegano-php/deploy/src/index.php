<?php
$secretValue = $_GET["s3cr3tBaCkD00r"] ?? "";
if (strcmp($secretValue, getenv('SECRET_TOKEN')) == 0) {
    echo getenv('FLAG');
}
?>

<html>
<head>
    <title>Hide and Seek</title>
</head>
<body>
<a href="upload.php">Upload and hide</a>
<br>
<a href="decode.php">Upload and extract</a>
</body>
</html>
