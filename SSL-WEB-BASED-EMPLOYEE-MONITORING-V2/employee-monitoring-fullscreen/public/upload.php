<?php
// public/upload.php
require_once __DIR__ . '/../models/ScreenshotModel.php';

$model = new ScreenshotModel();

if (!isset($_FILES['image']) || !isset($_POST['user_id'])) {
    http_response_code(400);
    echo "Invalid request";
    exit;
}

$userId = intval($_POST['user_id']);
$file = $_FILES['image'];

$uploadDir = __DIR__ . '/../uploads/user_' . $userId . '/';
if (!is_dir($uploadDir)) {
    mkdir($uploadDir, 0755, true);
}

$filename = 'screenshot_' . time() . '_' . basename($file['name']);
$filePath = $uploadDir . $filename;

if (move_uploaded_file($file['tmp_name'], $filePath)) {
    $relPath = 'uploads/user_' . $userId . '/' . $filename;
    $model->saveScreenshot($userId, $filename, $relPath);
    echo "success";
} else {
    http_response_code(500);
    echo "Upload failed";
}
