# VPA System

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Backend-Flask-black)
![Vue.js](https://img.shields.io/badge/Frontend-Vue.js-42b883)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-336791)
![Celery](https://img.shields.io/badge/Async-Celery-green)
![License](https://img.shields.io/badge/License-Private-red)

---

## 📌 Overview

VPA is a full-stack system built with:

- Flask backend (REST APIs)
- Vue.js frontend
- PostgreSQL database
- Celery workers for background jobs
- Postfix (Gmail SMTP relay) for email delivery

---

## 🧠 System Architecture

```mermaid
flowchart LR
U[User Browser] --> FE[Vue.js Frontend]
FE --> BE[Flask Backend API]
BE --> DB[(PostgreSQL Database)]
BE --> CEL[Celery Worker]
CEL --> CELB[Celery Beat Scheduler]
BE --> MAIL[Postfix SMTP Relay]
MAIL --> GMAIL[Gmail SMTP Server]
CEL --> DB
```

---

## ⚙️ Backend Setup (Flask + PostgreSQL)

### Requirements
- Python 3.11.11
- PostgreSQL running
- Virtual environment recommended

---

## 🗄️ Database Setup (PostgreSQL)

```bash
sudo -u postgres psql
```

```sql
CREATE DATABASE vpa_db;
CREATE USER vpa_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE vpa_db TO vpa_user;
```

### Environment Variable
```bash
DATABASE_URL=postgresql://vpa_user:your_password@localhost:5432/vpa_db
```

---

## 🧱 Database Migrations

```bash
cd vpa/beserver
flask db init
flask db migrate -m "initial tables"
flask db upgrade
```

---

## 🌱 Seed Database

```bash
flask seed
```

Default credentials:
- username: admin
- password: admin

---

## 🚀 Run Backend

```bash
python3.11 -m venv venv
source venv/bin/activate
python setup.py develop
cd vpa/backend
flask run
```

OR

```bash
python app.py
```

---

# 🎨 Frontend Setup (Vue.js)

- Node.js v22.19.0

```bash
cd vpa/feserver
npm install
npm run dev
```

### Production Build
```bash
npm run build
```

---

# ⚙️ Celery

### Worker
```bash
celery -A vpa.beserver.scheduler.celery_runner worker --loglevel=info
```

### Beat
```bash
celery -A vpa.beserver.scheduler.celery_runner beat --loglevel=info
```

---

# 📧 Email Setup (Postfix + Gmail SMTP)

```bash
sudo apt update
sudo apt install postfix mailutils -y
```

Configure:
- Internet Site
- Mail domain

---

## Gmail App Password
https://myaccount.google.com/apppasswords

---

## Postfix Config
Edit:
```bash
sudo nano /etc/postfix/main.cf
```

Add:
```
relayhost = [smtp.gmail.com]:587
smtp_sasl_auth_enable = yes
smtp_sasl_password_maps = hash:/etc/postfix/sasl_passwd
smtp_sasl_security_options = noanonymous
smtp_sasl_tls_security_options = noanonymous
smtp_use_tls = yes
smtp_tls_security_level = encrypt
smtp_tls_CAfile = /etc/ssl/certs/ca-certificates.crt
```

---

## Credentials
```
[smtp.gmail.com]:587 your_email@gmail.com:your_app_password
```

```bash
sudo chmod 600 /etc/postfix/sasl_passwd
sudo postmap /etc/postfix/sasl_passwd
sudo systemctl restart postfix
sudo systemctl enable postfix
```

---

## Test Email
```bash
echo "Test" | mail -s "Test Email" you@example.com
```
---

# 🧾 Project Structure

vpa/
- beserver/
- backend/
- feserver/
- scheduler/