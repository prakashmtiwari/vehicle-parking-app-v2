Project Setup


##Commands to migrate app

#Initialize migrations (first time only)
flask db init

#Generate migrations when models change
flask db migrate -m "initial tables"

#Apply migrations
flask db upgrade

#Seed the database with admin role and admin user with superuser priviledges
flask seed
