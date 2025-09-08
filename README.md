
# 🚗 Vehicle Parking Web App

A full-stack web application that allows users to view and book parking spots in various parking lots. Admins can manage lots, monitor reservations, and release a spot after collecting payment from the customer. They can also see the summary of past reservations.

---

## 📌 Features

- 🔐 User authentication (registration & login)
- 🅿️ View available parking lots and spots
- 📅 Reserve a spot instantly
- 🧾 Track past reservations and payments
- ⚙️ Admin dashboard to manage lots and spot availability
- 📊 Summary & Charts for past reservations for admin and user

## Folder Structure

# 📁 Project Folder Structure

This document outlines the structure of the `vehicle-parking-app/` project directory.

```
vehicle-parking-app/
├── instance/                        # Flask instance folder (e.g., configs, DB)
├── README.md                        # Project documentation
├── requirements.txt                 # Python dependencies
├── run.py                           # Entry point for the Flask app

├── vpa/                             # Main application package
│   ├── __init__.py                  # App factory / initialization
│   ├── models.py                    # SQLAlchemy models
│   ├── vpa_routes.py                # Route registration / blueprints

│   ├── resources/                   # RESTful API endpoints
│   │   ├── __init__.py
│   │   ├── lot_resource.py
│   │   └── spot_resource.py

│   ├── routes/                      # HTML-based view functions
│   │   └── __init__.py

│   ├── static/                      # Static files
│   │   └── images/
│   │       └── parking.png

│   └── templates/                   # Jinja2 templates
│       ├── base.html
│       ├── dash.html
│       ├── collect_payment_admin_modal.html
│       ├── confirm_payment_modal.html
│       ├── msg.html
│       ├── navbar.html
│       ├── search_results.html
│       ├── search_results_admin.html
│       ├── user_dash.html
│       ├── user_navbar.html
│       ├── user_parking_history.html
│       ├── user_parking_history_admin.html
│       └── users.html
```

## 🏗️ Tech Stack

| Layer       | Technology       |
|-------------|------------------|
| Frontend    | HTML, Jinja, CSS, JavaScript, Bootstrap |
| Backend     | Python (Flask), Flask-RESTful |
| Database    | SQLite3 / SQLAlchemy |
| Deployment  | localhost |

---


### 🔧 Prerequisites

- Python 3.10+
- pip

### 📦 Installation

```bash
git clone https://github.com/22f1000252/vehicle-parking-app.git
cd vehicle-parking-app
python3 -m venv venv
source venv/bin/activate    # or venv\Scripts\activate on Windows
pip install -r requirements.txt

## Run the APP

# python3 run.py


🙋‍♂️ Author
Prakash Tiwari – @22f1000252
