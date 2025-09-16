// public/assets/js/app.js
(() => {
  const startBtn = document.getElementById("startBtn");
  const pauseBtn = document.getElementById("pauseBtn");
  const stopBtn = document.getElementById("stopBtn");
  const statusEl = document.getElementById("status");

  let captureIntervalId = null;
  const INTERVAL_MS = 5 * 60 * 1000; // 5 minutes = 300000 ms
  // For quick testing you can set to 15000 (15 sec) then switch to 300000

  function updateStatus(text) {
    statusEl.innerText = "Status: " + text;
  }

  async function captureAndUpload() {
    try {
      // capture the visible page using html2canvas
      const canvas = await html2canvas(document.body);
      const dataUrl = canvas.toDataURL("image/png");
      // show preview small (optional)
      const prev = document.getElementById("preview");
      prev.innerHTML = `<img src="${dataUrl}" style="width:150px;border:1px solid #ccc" />`;

      // send to server
      const form = new FormData();
      form.append("image", dataUrl);
      form.append("user_id", USER_ID);

      const resp = await fetch("../public/index.php?action=save", {
        method: "POST",
        body: form,
      });
      const data = await resp.json();
      if (data.status === "success") {
        console.log("Saved", data.path);
      } else {
        console.warn("Save failed", data);
      }
    } catch (err) {
      console.error("Capture error", err);
    }
  }

  startBtn.addEventListener("click", () => {
    if (captureIntervalId) return;
    // immediate capture then set interval
    captureAndUpload();
    captureIntervalId = setInterval(captureAndUpload, INTERVAL_MS);
    startBtn.disabled = true;
    pauseBtn.disabled = false;
    stopBtn.disabled = false;
    updateStatus("Running");
  });

  pauseBtn.addEventListener("click", () => {
    if (!captureIntervalId) return;
    clearInterval(captureIntervalId);
    captureIntervalId = null;
    startBtn.disabled = false;
    pauseBtn.disabled = true;
    updateStatus("Paused");
  });

  stopBtn.addEventListener("click", async () => {
    // stop capturing
    if (captureIntervalId) {
      clearInterval(captureIntervalId);
      captureIntervalId = null;
    }
    startBtn.disabled = false;
    pauseBtn.disabled = true;
    stopBtn.disabled = true;
    updateStatus("Preparing ZIP...");

    // Request ZIP download from server. This will prompt browser to download the zip.
    // We add user_id param to identify user.
    const url = `../public/index.php?action=download&user_id=${encodeURIComponent(
      USER_ID
    )}`;

    // navigate to the download URL to trigger browser download
    window.location.href = url;

    updateStatus("Stopped — ZIP download started");
  });
})();
