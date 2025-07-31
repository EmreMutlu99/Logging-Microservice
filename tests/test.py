import requests

BASE_URL_SERVICE = "http://localhost:3005/post/service"
BASE_URL_LOG     = "http://localhost:3005/post/log"

def test_create_service(name, is_active=True):
    """Test creating a new service and retrieve its ID via GET."""
    print(f"Testing Service Creation: {name}...")
    payload = {"service_name": name, "is_active": is_active}
    resp = requests.post(BASE_URL_SERVICE, json=payload)
    assert resp.status_code in (200, 201), f"Failed ({resp.status_code}): {resp.text}"
    data = resp.json()
    assert data.get("status") == "success", f"Unexpected response: {data}"

    resp2 = requests.get(BASE_URL_SERVICE)
    assert resp2.status_code == 200, f"GET failed: {resp2.status_code}"
    services = resp2.json()
    matches = [s for s in services if s.get("service_name") == name]
    assert matches, f"Service '{name}' not found: {services}"
    service_id = matches[-1]["service_id"]
    print(f"✔ Service Creation Passed: ID={service_id}\n")
    return service_id

def test_get_services():
    print("Testing GET /service...")
    resp = requests.get(BASE_URL_SERVICE)
    assert resp.status_code == 200, f"Failed ({resp.status_code}): {resp.text}"
    data = resp.json()
    assert isinstance(data, list), f"Expected list, got {type(data)}"
    print(f"✔ GET /service returned {len(data)} services\n")


def test_user_specific_log(user_id, message, service_name):
    print(f"Testing User-Specific Log for User {user_id}...")
    payload = {
        "service_name": service_name,
        "user_id": user_id,
        "log_level": "INFO",
        "message": message,
        "log_timestamp": "2025-07-18T16:00:00Z"
    }
    resp = requests.post(BASE_URL_LOG, json=payload)
    assert resp.status_code == 200, f"Failed ({resp.status_code}): {resp.text}"
    data = resp.json()
    assert data.get("service_id") is not None, f"service_id missing: {data}"
    assert data["user_id"] == user_id, f"user_id mismatch: {data}"
    print("✔ User-Specific Log Test Passed\n")

def test_global_log(service_name, message="Global log test"):
    print("Testing Global Log Endpoint...")
    payload = {
        "service_name": service_name,
        "log_level": "ERROR",
        "message": message,
        "log_timestamp": "2025-07-18T16:05:00Z"
    }
    resp = requests.post(BASE_URL_LOG, json=payload)
    assert resp.status_code == 200, f"Failed ({resp.status_code}): {resp.text}"
    data = resp.json()
    assert data.get("service_id") is not None, f"service_id missing: {data}"
    print("✔ Global Log Test Passed\n")

def test_multiple_user_logs(service_name):
    print("Testing Logs for Multiple Users...")
    for uid in (101, 202, 303):
        test_user_specific_log(uid, f"Log for user {uid}", service_name)
    print("✔ Multiple User Log Test Passed\n")

def test_valid_timestamp():
    payload = {
        "user_id": 1,
        "service_name": "Messenger_Bot",
        "log_level": "INFO",
        "message": "Missing service_name",
        "log_timestamp": "2025-07-18T16:00:00Z"
    }
    resp = requests.post(BASE_URL_LOG, json=payload)
    assert resp.status_code == 200
    print("✔ Valid Timestamp Test Passed\n")


def test_no_timestamp():
    payload = {
        "user_id": 1,
        "service_name": "Messenger_Bot",
        "log_level": "INFO",
        "message": "Timestamp field deliberately omitted",
    }

    resp = requests.post(BASE_URL_LOG, json=payload)

    assert resp.status_code == 200, (
        f"Expected 200 OK since timestamp is server-side now, got {resp.status_code}.\n"
        f"Response content: {resp.text}"
    )

    data = resp.json()

    assert "log_timestamp" in data, "'log_timestamp' alanı eksik."
    assert data["log_timestamp"], "'log_timestamp' boş geldi."

    print("✔ test_no_timestamp passed.")




if __name__ == "__main__":
    print("\n=== Starting API Tests ===\n")

    # 1) Test Service endpoint
    print("---- Service Endpoint Tests ----")
    sid = test_create_service("PyTest_Service")       
    test_get_services()

    # 2) Test Log endpoints
    print("---- Log Endpoint Tests ----")
    test_create_service("EmailNotification")          
    test_user_specific_log(42, "Initial log for user 42", "EmailNotification")
    test_global_log("EmailNotification")
    test_multiple_user_logs("EmailNotification")

    # 3) Time Stamp
    test_valid_timestamp()
    test_no_timestamp()
    
    print("=== All Tests Completed Successfully ===\n")
