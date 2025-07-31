import requests

class LoggingClient:
    BASE_URL = "http://localhost:3005/post/log"

    def log(self, service_name, log_level, message, user_id=None):
        """
        Send a log message to the logging service.
        :param service_name: Name of the service generating the log.
        :param log_level: Log level (e.g., INFO, ERROR).
        :param message: Log message content.
        :param user_id: User ID for user-specific logs. None for user-independent logs.
        """
        payload = {
            "service_name": service_name,
            "log_level": log_level,
            "message": message
        }
        if user_id:
            payload["user_id"] = user_id

        try:
            response = requests.post(self.BASE_URL, json=payload)
            response.raise_for_status()
            print(f"Log successfully sent: {response.json()}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to send log: {e}")

deneme = LoggingClient()
deneme.log(log_level="INFO",message="Message Log",service_name="Example_Service",user_id=3)