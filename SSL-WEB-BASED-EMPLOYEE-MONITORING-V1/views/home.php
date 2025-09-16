<?php
// views/home.php
// In a real system use sessions and actual user login. For now we assume $userId = 1
session_start();
$userId = isset($_SESSION['user_id']) ? intval($_SESSION['user_id']) : 1;
?>
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Employee Monitoring - Home</title>
  <link rel="stylesheet" href="../public/assets/css/style.css">
</head>
<body>
  <div class="container">
    <h1>Employee Monitoring</h1>
    <div class="controls">
      <button id="startBtn">Start</button>
      <button id="pauseBtn" disabled>Pause</button>
      <button id="stopBtn" disabled>Stop</button>
    </div>
    <p id="status">Status: Idle</p>
    <div id="preview"></div>
  </div>

  <script>
    // expose user id for JS
    const USER_ID = <?php echo json_encode($userId); ?>;
  </script>
  <script src="https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js"></script>
  <script src="../public/assets/js/app.js"></script>
</body>
</html>
