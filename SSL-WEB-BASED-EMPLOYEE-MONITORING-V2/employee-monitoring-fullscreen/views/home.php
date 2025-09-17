<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Employee Monitoring</title>
  <link rel="stylesheet" href="assets/style.css">
</head>
<body>
  <h1>Employee Monitoring System</h1>
  <div class="controls">
    <button onclick="setStatus('started')">Start</button>
    <button onclick="setStatus('paused')">Pause</button>
    <button onclick="setStatus('stopped')">Stop</button>
  </div>

  <script>
    function setStatus(status) {
      fetch("index.php?action=" + status)
        .then(res => {
          if (status === 'stopped') {
            return res.blob().then(blob => {
              const link = document.createElement("a");
              link.href = URL.createObjectURL(blob);
              link.download = "screenshots.zip";
              link.click();
            });
          } else {
            return res.json().then(data => alert(data.message));
          }
        })
        .catch(err => console.error(err));
    }
  </script>
</body>
</html>
