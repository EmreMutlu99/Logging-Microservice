class LoggingClient {
  constructor() {
    this.BASE_URL = "http://localhost:3005/post/log";
  }

  async log({ service_name, log_level, message, user_id = null }) {
    const payload = {
      service_name,
      log_level,
      message,
    };

    if (user_id !== null) {
      payload.user_id = user_id;
    }

    try {
      const response = await fetch(this.BASE_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      console.log("Log successfully sent:", data);
    } catch (error) {
      console.error("Failed to send log:", error);
    }
  }
}

// Tested and worked. Open JS CLIENT comment line in the index.html to try


// Example
const logger = new LoggingClient();
logger.log({
  service_name: "Desktop-App",
  log_level: "INFO",
  message: "DENEME LOG MESAJ",
  user_id: 3,
});
