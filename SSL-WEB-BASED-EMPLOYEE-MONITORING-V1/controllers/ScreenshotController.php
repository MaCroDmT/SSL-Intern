<?php
// controllers/ScreenshotController.php
require_once __DIR__ . '/../models/ScreenshotModel.php';

class ScreenshotController {
    private $model;
    private $uploadDir;

    public function __construct(){
        $this->model = new ScreenshotModel();
        $this->uploadDir = __DIR__ . '/../uploads/';
        if (!is_dir($this->uploadDir)) {
            mkdir($this->uploadDir, 0755, true);
        }
    }

    // Save image posted as base64 via AJAX
    public function save() {
        // Example: you should replace this with session user id in real app
        $userId = isset($_POST['user_id']) ? intval($_POST['user_id']) : 1;

        if (!isset($_POST['image'])) {
            http_response_code(400);
            echo json_encode(['status'=>'error','message'=>'No image']);
            exit;
        }

        $img = $_POST['image'];
        // $img like "data:image/png;base64,...."
        if (preg_match('/^data:image\/(\w+);base64,/', $img, $type)) {
            $data = substr($img, strpos($img, ',') + 1);
            $type = strtolower($type[1]); // png, jpg, gif

            if (!in_array($type, ['png','jpg','jpeg','gif'])) {
                http_response_code(415);
                echo json_encode(['status'=>'error','message'=>'Unsupported image type']);
                exit;
            }

            $data = base64_decode($data);
            if ($data === false) {
                http_response_code(400);
                echo json_encode(['status'=>'error','message'=>'Base64 decode failed']);
                exit;
            }

            $userFolder = $this->uploadDir . 'user_' . $userId . '/';
            if (!is_dir($userFolder)) mkdir($userFolder, 0755, true);

            $filename = 'screenshot_' . time() . '_' . bin2hex(random_bytes(4)) . '.' . $type;
            $filePath = $userFolder . $filename;
            file_put_contents($filePath, $data);

            // Save DB relative path
            $relPath = 'uploads/user_' . $userId . '/' . $filename;
            $ok = $this->model->saveScreenshot($userId, $filename, $relPath);

            if ($ok) {
                echo json_encode(['status'=>'success','path'=>$relPath]);
            } else {
                http_response_code(500);
                echo json_encode(['status'=>'error','message'=>'DB save failed']);
            }
            exit;
        } else {
            http_response_code(400);
            echo json_encode(['status'=>'error','message'=>'Invalid image data']);
            exit;
        }
    }

    // Create ZIP of user's screenshots and force download
    public function downloadZip() {
    // Increase PHP execution limits for big zips
    ini_set('max_execution_time', 0); // unlimited
    ini_set('memory_limit', '512M');  // increase if needed

    $userId = isset($_GET['user_id']) ? intval($_GET['user_id']) : 1;

    $records = $this->model->getUserScreenshots($userId);
    if (empty($records)) {
        http_response_code(404);
        echo "No screenshots found.";
        exit;
    }

    $zipName = 'screenshots_user_' . $userId . '_' . time() . '.zip';
    $tmpZip = sys_get_temp_dir() . '/' . $zipName;

    $zip = new \ZipArchive();
    if ($zip->open($tmpZip, \ZipArchive::CREATE) !== true) {
        http_response_code(500);
        echo "Failed to create ZIP.";
        exit;
    }

    // Add files in chunks to avoid MySQL timeout
    foreach ($records as $r) {
        $fullPath = __DIR__ . '/../' . $r['file_path'];
        if (file_exists($fullPath)) {
            $zip->addFile($fullPath, $r['filename']);
        }
    }

    $zip->close();

    // Send ZIP file
    header('Content-Type: application/zip');
    header('Content-Disposition: attachment; filename="' . basename($tmpZip) . '"');
    header('Content-Length: ' . filesize($tmpZip));
    flush();
    readfile($tmpZip);
    unlink($tmpZip);
    exit;
}


    // Optionally: delete the user's screenshots after zipping
    public function deleteAll($userId) {
        // not used by default; implement if you want to remove DB entries + files
    }
}
