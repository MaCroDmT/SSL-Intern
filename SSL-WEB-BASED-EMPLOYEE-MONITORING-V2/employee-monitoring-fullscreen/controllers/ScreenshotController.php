<?php
// controllers/ScreenshotController.php
require_once __DIR__ . '/../models/ScreenshotModel.php';

class ScreenshotController {
    private $model;
    private $uploadDir;
    private $storagePath;
    public function __construct() {
    // Existing model
    $this->model = new ScreenshotModel();

    // Directory to save screenshots
    $this->storagePath = __DIR__ . '/../storage/screenshots/';
    if (!is_dir($this->storagePath)) {
        mkdir($this->storagePath, 0777, true);
    }
}


    // Update session state
    public function setStatus($status) {
        $userId = 1; // static for now
        $this->model->updateSessionStatus($userId, $status);

        if ($status === 'stopped') {
            $this->downloadTodaysZip($userId);
        } else {
            echo json_encode(["status" => "ok", "message" => "Session $status"]);
        }
    }

     // ✅ NEW method — just add this, don’t remove the old code
    public function save() {
    require_once __DIR__ . '/../models/Database.php';
    $db = (new Database())->getConnection();

    if (!isset($_POST['user_id']) || !isset($_POST['image'])) {
        http_response_code(400);
        echo "Missing parameters";
        return;
    }

    $userId = intval($_POST['user_id']);
    $imageData = $_POST['image'];

    if (strpos($imageData, "base64,") !== false) {
        $imageData = explode("base64,", $imageData)[1];
    }

    $decoded = base64_decode($imageData);
    if ($decoded === false) {
        http_response_code(400);
        echo "Invalid base64 data";
        return;
    }

    // save to file system
    $filename = $this->storagePath . "user_" . $userId . "_" . time() . ".png";
    file_put_contents($filename, $decoded);

    // save to database
    $stmt = $db->prepare("INSERT INTO screenshots (user_id, image, created_at) VALUES (?, ?, NOW())");
    $null = NULL;
    $stmt->bind_param("ib", $userId, $null);
    $stmt->send_long_data(1, $decoded);
    $stmt->execute();
    $stmt->close();

    echo json_encode(["message" => "Screenshot saved", "file" => basename($filename)]);
}

    // Download today's screenshots as zip
    public function downloadTodaysZip($userId) {
        ini_set('max_execution_time', 0);
        ini_set('memory_limit', '512M');

        $records = $this->model->getTodaysScreenshots($userId);
        if (empty($records)) {
            echo "No screenshots for today.";
            exit;
        }

        $zipName = 'screenshots_' . date("Y-m-d") . '.zip';
        $tmpZip = sys_get_temp_dir() . '/' . $zipName;

        $zip = new \ZipArchive();
        if ($zip->open($tmpZip, \ZipArchive::CREATE) !== true) {
            echo "Failed to create zip";
            exit;
        }

        foreach ($records as $r) {
            $fullPath = __DIR__ . '/../' . $r['file_path'];
            if (file_exists($fullPath)) {
                $zip->addFile($fullPath, $r['filename']);
            }
        }

        $zip->close();

        header('Content-Type: application/zip');
        header('Content-Disposition: attachment; filename="' . basename($tmpZip) . '"');
        header('Content-Length: ' . filesize($tmpZip));
        flush();
        readfile($tmpZip);
        unlink($tmpZip);
        exit;
    }
}
