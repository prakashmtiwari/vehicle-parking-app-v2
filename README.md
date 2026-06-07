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

- **Flask backend (REST APIs)**
- **Vue.js frontend**
- **PostgreSQL database**
- **Celery workers for background jobs**
- **Postfix (Gmail SMTP relay) for email delivery**

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


⚙️ Backend Setup (Flask + PostgreSQL)

📦 Requirements
Python 3.11.11
PostgreSQL running
Virtual environment recommended


🗄️ Database Setup (PostgreSQL)

sudo -u postgres psql
CREATE DATABASE vpa_db;
CREATE USER vpa_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE vpa_db TO vpa_user;

Set environment variable:
DATABASE_URL=postgresql://vpa_user:your_password@localhost:5432/vpa_db


🧱 Database Migrations

cd vpa/beserver

Initialize migrations

flask db init
Create migration
flask db migrate -m "initial tables"

Apply migration

flask db upgrade


🌱 Seed Database

flask seed

Default admin credentials:

Username: admin
Password: admin

🚀 Run Backend

python3.11 -m venv venv
source venv/bin/activate
python setup.py develop
cd vpa/backend
flask run

OR

python app.py


🎨 Frontend Setup (Vue.js)

📦 Node Version
Node.js v22.19.0

🧩 Install & Run
cd vpa/feserver
npm install
npm run dev
🏗️ Production Build
npm run build


⚙️ Celery Setup

▶️ Start Worker
celery -A vpa.beserver.scheduler.celery_runner worker --loglevel=info

⏱️ Start Scheduler
celery -A vpa.beserver.scheduler.celery_runner beat --loglevel=info

📧 Email System (Postfix + Gmail SMTP)
📦 Install Postfix
sudo apt update
sudo apt install postfix mailutils -y

Select:

Internet Site
Mail name: your domain (e.g. example.com)
🔐 Gmail App Password Setup
Enable 2FA: https://myaccount.google.com/security

Create App Password: https://myaccount.google.com/apppasswords

⚙️ Configure Postfix
sudo nano /etc/postfix/main.cf

Add:

relayhost = [smtp.gmail.com]:587

smtp_sasl_auth_enable = yes
smtp_sasl_password_maps = hash:/etc/postfix/sasl_passwd
smtp_sasl_security_options = noanonymous
smtp_sasl_tls_security_options = noanonymous

smtp_use_tls = yes
smtp_tls_security_level = encrypt
smtp_tls_CAfile = /etc/ssl/certs/ca-certificates.crt

🔑 Credentials
sudo nano /etc/postfix/sasl_passwd
[smtp.gmail.com]:587 your_email@gmail.com:your_app_password

🔒 Secure Setup
sudo chmod 600 /etc/postfix/sasl_passwd
sudo postmap /etc/postfix/sasl_passwd
sudo systemctl restart postfix
sudo systemctl enable postfix

🧪 Test Email
echo "Test email body" | mail -s "Test Email" you@example.com
📜 Logs
sudo tail -f /var/log/mail.log

📊 Scheduled Reports


🧾 Project Structure
vpa/
├── beserver/        # Flask backend
├── backend/         # API entrypoint
├── feserver/        # Vue frontend
├── scheduler/       # Celery tasks
└── instance/        # Local configs (Postgres setup)


🚀 Key Features
Role-based authentication
PostgreSQL persistence layer
Background task processing (Celery)
Scheduled reporting system
Email notifications via SMTP relay
Vue.js SPA frontend