// 🌐 Global State
let selectedServiceName = null;
const logsByService = {};

// 📦 DOM Elements
// -- Sidebar
const serviceList = document.getElementById("serviceList");
const addServiceBtn = document.getElementById("addServiceBtn");
const removeServiceBtn = document.getElementById("removeServiceBtn");
const addServiceForm = document.getElementById("addServiceForm");
const newServiceNameInput = document.getElementById("newServiceName");
const confirmAddServiceBtn = document.getElementById("confirmAddServiceBtn");
const cancelAddServiceBtn = document.getElementById("cancelAddServiceBtn");
const allLogsBtn = document.getElementById("allLogsBtn");

// -- Filters & Controls
const logFilter = document.getElementById("logFilter");
const sortOrder = document.getElementById("sortOrder");
const userIdFilter = document.getElementById("userIdFilter");
const autoRefreshToggle = document.getElementById("autoRefreshToggle");
const manualRefreshBtn = document.getElementById("manualRefreshBtn");

// -- Main & Popup
const selectedServiceSpan = document.getElementById("selectedServiceName");
const logContainer = document.getElementById("logContainer");
const popup = document.getElementById("popup");
const popupContent = document.getElementById("popupContent");
const closePopup = document.getElementById("closePopup");

// 🔁 Auto Refresh Interval
let autoRefreshInterval = null;

// Fetch all services into the sidebar*/
function fetchServices() {
  fetch("/get/service")
    .then(res => res.json())
    .then(services => {
      serviceList.innerHTML = '';
      services.forEach(service => {
        const li = document.createElement("li");
        li.textContent = service.service_name;

        li.addEventListener("click", () => {
          document.querySelectorAll("#serviceList li").forEach(li => li.classList.remove("active"));
          li.classList.add("active");
          selectService(service.service_name);
        });

        serviceList.appendChild(li);
      });
    })
    .catch(err => console.error("🚫 Servisler alınamadı:", err));
}

// Fetch logs according to a service 
function fetchLogsForService(serviceName) {
  fetch("/get/log")
    .then(res => res.json())
    .then(allLogs => {
      const logs = allLogs
        .filter(log => log.service?.service_name === serviceName)
        .map(log => ({
          id: log.log_id,
          user_id: log.user_id,
          message: log.message,
          timestamp: log.log_timestamp,
          level: log.log_level
        }));

      logsByService[serviceName] = logs;
      filterAndSortLogs();
    })
    .catch(err => console.error("🚫 Cannot Fetch Logs:", err));
}

// Fetch all services' logs
function fetchAllLogs() {
  fetch("/get/log")
    .then(res => res.json())
    .then(allLogs => {
      const logs = allLogs.map(log => ({
        id: log.log_id,
        user_id: log.user_id,
        message: log.message,
        timestamp: log.log_timestamp,
        level: log.log_level,
        service: log.service?.service_name || null
      }));

      logsByService["All Logs"] = logs;
      filterAndSortLogs();
    })
    .catch(err => console.error("🚫 Cannot Fetch All Logs:", err));
}

// Filtering and Sorting
function filterAndSortLogs() {
  let logs = [];

  if (selectedServiceName === "All Logs") {
    logs = logsByService["All Logs"] || [];
  } else if (selectedServiceName) {
    logs = logsByService[selectedServiceName] || [];
  }

  const selectedLevel = logFilter.value;
  if (selectedLevel !== "all") {
    logs = logs.filter(log => log.level.toUpperCase() === selectedLevel);
  }

  const userIdValue = userIdFilter.value.trim();
  if (userIdValue !== "") {
    logs = logs.filter(log => String(log.user_id) === userIdValue);
  }

  const order = sortOrder.value;
  logs.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
  if (order === "desc") logs.reverse();

  renderLogs(logs);
}

// Rendering logs
function renderLogs(logs) {
  logContainer.innerHTML = '';

  logs.forEach(log => {
    const row = document.createElement("div");
    row.classList.add("log-row");
    row.innerHTML = `
      <div>${log.id}</div>
      <div>${log.user_id}</div>
      <div>${log.message}</div>
      <div>${new Date(log.timestamp).toLocaleString()}</div>
      <div>${log.level}</div>
    `;
    row.addEventListener("click", () => {
      popupContent.textContent = JSON.stringify(log, null, 2);
      popup.classList.remove("hidden");
    });
    logContainer.appendChild(row);
  });
}

// Fetch logs when a service is selected
function selectService(serviceName) {
  selectedServiceName = serviceName;
  selectedServiceSpan.textContent = serviceName ? `'${serviceName}' Logs` : 'All Logs';

  if (!serviceName || serviceName === "All Logs") {
    fetchAllLogs();
  } else {
    fetchLogsForService(serviceName);
  }
}

// Add new service
confirmAddServiceBtn.addEventListener("click", () => {
  const name = newServiceNameInput.value.trim();
  if (!name) {
    alert("Please enter a service name.");
    return;
  }

  fetch("/post/service", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ service_name: name })
  })
    .then(res => {
      if (!res.ok) throw new Error("Cannot add service");
      return res.json();
    })
    .then(() => {
      newServiceNameInput.value = "";
      addServiceForm.classList.add("hidden");
      fetchServices();
    })
    .catch(err => alert("🚫 " + err.message));
});

// Delete a service and it's logs
removeServiceBtn.addEventListener("click", () => {
  if (!selectedServiceName || selectedServiceName === "All Logs") return;

  const confirmDelete = confirm(`Are you sure you want to delete the '${selectedServiceName}' service and all logs associated with it?`);
  if (!confirmDelete) return;

  fetch(`/delete/service/${encodeURIComponent(selectedServiceName)}`, {
    method: "DELETE"
  })
    .then(res => {
      if (!res.ok) throw new Error("Deletion Failed");
      return res.json();
    })
    .then(() => {
      alert("✅ Service is deleted");
      selectedServiceName = null;
      selectedServiceSpan.textContent = '';
      logContainer.innerHTML = '';
      fetchServices();
    })
    .catch(err => alert("🚫 " + err.message));
});

// Fetch all logs when button is clicked
allLogsBtn.addEventListener("click", () => {
  document.querySelectorAll("#serviceList li").forEach(li => li.classList.remove("active"));
  selectService("All Logs");
});

// Closing pop-up
closePopup.addEventListener("click", () => {
  popup.classList.add("hidden");
});

// Showing snackbar notifications
function showSnackbar(message, duration = 3000) {
  const snackbar = document.getElementById("snackbar");
  snackbar.textContent = message;
  snackbar.classList.add("show");
  setTimeout(() => {
    snackbar.classList.remove("show");
  }, duration);
}

// New service button process
addServiceBtn.addEventListener("click", () => {
  addServiceForm.classList.toggle("hidden");
  if (!addServiceForm.classList.contains("hidden")) {
    newServiceNameInput.focus();
  }
});
cancelAddServiceBtn.addEventListener("click", () => {
  addServiceForm.classList.add("hidden");
  newServiceNameInput.value = "";
});
newServiceNameInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") confirmAddServiceBtn.click();
});

// Watching filter changes
logFilter.addEventListener("change", filterAndSortLogs);
sortOrder.addEventListener("change", filterAndSortLogs);
userIdFilter.addEventListener("input", filterAndSortLogs);

// Checking auto refresh
autoRefreshToggle.addEventListener("change", () => {
  if (autoRefreshToggle.checked) {
    autoRefreshInterval = setInterval(() => {
      if (selectedServiceName === "All Logs") {
        selectService("All Logs");
      } else if (selectedServiceName) {
        fetchLogsForService(selectedServiceName);
      }
    }, 5000);

    showSnackbar("✅ Auto Refresh: 5 seconds enabled");
  } else {
    clearInterval(autoRefreshInterval);
    showSnackbar("🔕 Auto Refresh disabled");
  }
});

// Manual refresh logs button
manualRefreshBtn.addEventListener("click", () => {
  if (selectedServiceName === "All Logs") {
    fetchAllLogs();
  } else if (selectedServiceName) {
    fetchLogsForService(selectedServiceName);
  }
  showSnackbar("🔁 Logs refreshed");
});

// Fetch services when page is loaded
document.addEventListener("DOMContentLoaded", fetchServices);


/*

<------ These are optional manual log processes------>

// Manual log inserting
function sendLog(serviceName, message, level = "INFO", user_id = 0) {
  fetch("/post/log", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      service_name: serviceName,
      user_id: user_id,
      log_level: level,
      message: message
    })
  })
    .then(res => res.json())
    .then(data => {
      console.log("✅ Log eklendi:", data);
      fetchLogsForService(serviceName);
    })
    .catch(err => console.error("🚫 Cannot send the log:", err));
}
*/

/*
// Manual log deleting
function deleteLog(logId) {
  fetch(`/delete/log/${logId}`, {
    method: "DELETE"
  })
    .then(res => res.json())
    .then(() => {
      console.log("🗑️ Log is deleted");
      if (selectedServiceName) fetchLogsForService(selectedServiceName);
    });
}
*/
