# Use-Case and Context

In a production environment, event logs must be recorded. Some companies do this by saving events to text files, while others have their own logging systems in place. This project is a plugin-based solution that stores event logs in a database and provides a front-end interface for in-server monitoring.

It works as follows: any microservice running on the server makes a POST request to the logger orchestrator microservice provided in this project whenever an important event occurs. The orchestrator then saves the information into the database and serves as a gateway to provide an interactive front-end interface for monitoring the logs.

---
# Logger Service

A centralized logging system designed to collect logs from multiple independent services and display them through a user-friendly web interface. The application is ideal for internal log tracking within companies and provides both RESTful API endpoints and a responsive frontend dashboard.

![Logger Service Flow](assets/dashboard.png)

---

## Requirements

This project is designed to run **only on Linux systems** and requires the following dependencies:

- ✅ **PostgreSQL 16.4** – Ensure it's installed and running  
- 🐳 **Docker** – Required to run the logging service container  
- 🐍 **Python** – Required to install Prisma

> ⚠️ Make sure you have **PostgreSQL 16.4** installed and accessible. The logger service is tested with this specific version.



## How to Run


### 1. .env Setup
.env file must be also in the /prisma directory. So if .env doesn't exist in /prisma directory:
```env
cp .env /prisma/.env
```
💡 Or manually create.

#### .env Example

```env
SERVER_TYPE=development
DATABASE_URL=postgresql://user:password@localhost:5432/Logger
```
---


### 2. Apply Database Schema (First Time Only) 

> ⚠️ Note:
> If you're running the project on a clean PostgreSQL instance (no tables created yet), run:
>
> ```bash
> # to check prisma
> pip install prisma 
> prisma db push
> ```
> to apply the schema to the database.

### 3. Quick Start

To reach ./docker_run.sh options:
```bash
# Help
./docker_run.sh --help
```

Execute commands:
```bash
# Without rebuild
sudo ./docker_run.sh
```
or
```bash
# With rebuild
sudo ./docker_run.sh --build
```

### 4. Access Frontend

```
http://127.0.0.1:3005/index.html
```



---

## ✨ Features

* Collect logs from multiple services (e.g., bots, apps, scripts)
* Visualize logs in a clean web UI (`localhost:3005/index.html`)
* Filter logs by service, log level, or user ID
* Create and delete services dynamically
* PostgreSQL-backed storage using Prisma ORM

![Logger Service Flow](assets/logger_diagram.svg)

---


## 🧱 Tech Stack

* **Backend:** FastAPI, Prisma ORM
* **Frontend:** HTML + CSS + Vanilla JavaScript
* **Database:** PostgreSQL 16.4 (external, not containerized)
* **Dev Tools:** Docker, pgAdmin 9.5
* **Python:** 3.10.12

---


## 📊 API Endpoints

### Services

* `GET /get/service` → List all services
* `POST /post/service` → Register new service
* `DELETE /delete/service/{service_name}` → Delete service and its logs

### Logs

* `GET /get/log` → Retrieve all logs (with service name)
* `POST /post/log` → Add a new log entry

### UI

* `GET /index` → Serves the log panel (or use `/static/index.html`)

---

## 🔧 Example Requests

### POST /post/log

```json
{
  "service_name": "Auth-Service",
  "user_id": 42,
  "log_level": "ERROR",
  "message": "Failed to generate JWT token due to missing secret key."}
```

### POST /post/service

```json
{
  "service_name": "Slack-Service",
  "is_active": true
}
```

## 🌍 License

This project is licensed under the [MIT License](LICENSE).

It is open-source and free to use, modify, and distribute — for both personal and commercial purposes.

---

## 👤 Authors

**Ozan Uslan**


* GitHub: [uslanozan](https://github.com/uslanozan)
* LinkedIn: [linkedin.com/in/uslanozan](https://linkedin.com/in/uslanozan)
* Email: [uslanozan@gmail.com](mailto:uslanozan@gmail.com)

**Emre Mutlu**

* GitHub: [emremutlu99](https://github.com/emremutlu99)
* LinkedIn: [linkedin.com/in/emre-m-0899b4111](https://linkedin.com/in/emre-m-0899b4111)
* Email: [emre.mutlu@sagel-ai.com](mailto:emre.mutlu@sagel-ai.com)

---

## ➕ Optional Future Improvements
* Project architecture diagram
* Docker Compose support
* Dark mode toggle
