Project Setup

Backend
##Commands to set up database migrate it.

# Initialize migrations (first time only). Go to the folder ./vpa/beserver and run
flask db init

# Generate migrations when models change
flask db migrate -m "initial tables"

# Apply migrations
flask db upgrade

# Seed the database with admin role and admin user with superuser priviledges. Run from vpa/beserver
flask seed

# default username and password for admin is "admin"
 

#Run the backend server
# Create virtual environment with python 3.11.11
python3.11 -m venv venv

# Activate the venv
source venv/bin/activate

python setup.py develop

# Go to vpa/backend
flask run      ||    python app.py


# Frontend 
node
v22.19.0
# install vue js
npm create vue@latest

cd vpa/feserver
npm install
npm run dev


# For production
npm run build



# Start Celery worker 
celery -A vpa.beserver.scheduler.celery_runner worker --loglevel=info

# Start Celery beat (for scheduled tasks)
celery -A vpa.beserver.scheduler.celery_runner beat --loglevel=info



# Setup postfix for sending email
sudo apt update
sudo apt install postfix mailutils -y

During installation:

Choose "Internet Site"

Set your server’s mail name (e.g. example.com)


🔑  Enable App Password in Gmail
Go to Google Account Security
https://myaccount.google.com/security

Enable 2-Step Verification

https://myaccount.google.com/apppasswords
Under App passwords, choose:

App: Mail
Device: Other (Custom name) → e.g., “Postfix server”

Copy the 16-character password 



✍️  Configure Postfix to use Gmail as a relay

sudo nano /etc/postfix/main.cf

Add (or update) the following lines at the bottom:

# Use Gmail SMTP relay
relayhost = [smtp.gmail.com]:587

# Enable SASL authentication
smtp_sasl_auth_enable = yes
smtp_sasl_password_maps = hash:/etc/postfix/sasl_passwd
smtp_sasl_security_options = noanonymous
smtp_sasl_tls_security_options = noanonymous

# Use STARTTLS encryption
smtp_use_tls = yes
smtp_tls_security_level = encrypt
smtp_tls_CAfile = /etc/ssl/certs/ca-certificates.crt

# (Optional) Always use TLS
smtp_tls_loglevel = 1
smtp_tls_session_cache_database = btree:${data_directory}/smtp_scache


🔐  Create the SASL password file

sudo nano /etc/postfix/sasl_passwd

Add your Gmail credentials (use your full Gmail address):

[smtp.gmail.com]:587 your_email@gmail.com:your_app_password



🔒  Secure and hash the credentials

sudo chmod 600 /etc/postfix/sasl_passwd
sudo postmap /etc/postfix/sasl_passwd

This creates /etc/postfix/sasl_passwd.db, which Postfix will actually use.


🔄 Restart Postfix
sudo systemctl restart postfix
sudo systemctl enable postfix


🧪 Test sending email
echo "This is a test email body" | mail -s "Test Email" you@example.com

#Check logs 
sudo tail -f /var/log/mail.log





#For sending the monthly report of previous month change in vpa/beserver/tasks/reports.py  line number 255 uncomment and comment 256
