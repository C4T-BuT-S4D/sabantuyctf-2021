<?php

function endsWith($haystack, $needle)
{
    $length = strlen($needle);
    if (!$length) {
        return true;
    }
    return substr($haystack, -$length) === $needle;
}

function stringToBinary($string)
{
    $bin = "";
    for ($i = 0; $i < strlen($string); $i++) {
        $bin .= str_pad(decbin(ord($string[$i])), 8, '0', STR_PAD_LEFT);
    }

    return $bin;
}


function mask($byte, $bit1, $bit2)
{
    $x = str_pad(decbin($byte), 8, '0', STR_PAD_LEFT);
    $x[8 - 1] = $bit1;
    $x[8 - 2] = $bit2;
    return bindec($x);
}

const MAX_FILE_SIZE = 512 * 1024; // 512KB


if ($_FILES['userfile']['size'] == 0) {
    die("No file found");
}

if ($_FILES['userfile']['size'] > MAX_FILE_SIZE) {
    die("File is too big: the max size is " . strval(MAX_FILE_SIZE) . " bytes.");
}

$fileName = basename($_FILES['userfile']['name']);

//if (!endsWith($fileName, ".jpg") && !endsWith($fileName, ".jpeg")) {
//    die("Only .jpg/.jpeg files are supported");
//}

//if (mime_content_type($_FILES['userfile']['tmp_name']) !== 'image/jpeg') {
//    die("Invalid jpeg provided");
//}


if (!endsWith($fileName, ".png")) {
    die("Only .png files are supported");
}

if (mime_content_type($_FILES['userfile']['tmp_name']) !== 'image/png') {
    die("Invalid png image provided");
}

$text = $_POST['text'] ?? "";
$url = $_POST['url'] ?? "";

$ctx = stream_context_create(array('http' =>
    array(
        'timeout' => 10,  //10 secs
    )
));

if ($url !== "") {
    $text = file_get_contents($url, false, $ctx);
}

if ($text == "") {
    die("No text given");
}

$img = imagecreatefrompng($_FILES['userfile']['tmp_name']);

// Get image dimensions.
$width = imagesx($img);
$height = imagesy($img);

if ($width * $height * 4 < strlen($text)) {
    die("The provided image is too small to fit the text");
}

$binString = stringToBinary($text);
$pos = 0;
for ($i = 0; $i < $height; $i++) {
    for ($j = 0; $j < $width; $j++) {
        if ($pos >= strlen($binString)) {
            break 2;
        }
        $rgb = imagecolorat($img, $j, $i);
        $colors = imagecolorsforindex($img, $rgb);
        $red = $colors['red'];
        $green = $colors['green'];
        $blue = $colors['blue'];
        $alpha = $colors['alpha'];

        $red = mask($red, $binString[$pos] ?? "0", $binString[$pos+1] ?? "0");
        $blue = mask($blue, $binString[$pos+2] ?? "0", $binString[$pos+3] ?? "0");
        $newColor = imagecolorallocatealpha($img, $red, $green, $blue, $alpha);
        imagesetpixel($img, $j, $i, $newColor);
        $pos += 4;
    }
}

$tmpFILE = tmpfile();
$tmpPath = stream_get_meta_data($tmpFILE)['uri'];


if (!imagepng($img, $tmpPath, 9)) {
    die("Failed to create png image");
}

imagedestroy($img);

$newName = "steg_" . $fileName;
// It will be called downloaded.pdf
header("Content-Disposition: attachment; filename=\"${newName}\"");

readfile($tmpPath);

fclose($tmpFILE);