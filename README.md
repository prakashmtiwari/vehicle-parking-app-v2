Project Setup

Backend
##Commands to set up database migrate it.

#Initialize migrations (first time only). Go to the folder ./vpa/backend and runs
flask db init

#Generate migrations when models change
flask db migrate -m "initial tables"

#Apply migrations
flask db upgrade

#Seed the database with admin role and admin user with superuser priviledges
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


# Start Celery worker 
celery -A vpa.beserver.scheduler.celery_runner worker --loglevel=info

# Start Celery beat (for scheduled tasks)
celery -A vpa.beserver.scheduler.celery_runner beat --loglevel=info




#Frontend 

#install vue js
npm create vue@latest

cd vpa/feserver
npm install
npm run dev


# For production
npm run build



