<html>
<head>
    <title>Hide and Seek</title>
</head>
<body>
<h3>Upload an image to hide the text</h3>
<hr>
<form method="post" action="hide.php" enctype="multipart/form-data">
    Select PNG image to upload (max 512kb):
    <br>
    <br>
    <input type="file" name="userfile" id="fileToUpload">
    <br>
    <br>
    <label>
        Enter text to hide:
        <input type="text" name="text" placeholder="secret">
    </label>
    <br>
    <br>
    <label>
        or even get text from site URL:
        <input type="text" name="url" placeholder="https://cs-sabantuy.ru/robots.txt">
    </label>
    <br>
    <br>
    <input type="submit" value="Hide text!">
</form>
</body>
</html>