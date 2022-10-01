# postcodes
Practice for API postcodes


# Installation

for install create a environment with pyenv and run

    <code>pip install -r requirements.txt</code>
    <code>python manage.py createsuperuser</code>

with superuser open browser and navigate to admin <code>http://127.0.0.1:8000/admin</code>


# Run Django Rest Framework

for run server web run 

    <code>python manage.py runserver</code> 

into file_path api


# Database

use postgresql, run docker for postgres

    <code>docker pull postgres</code>
    <code>docker run --name YOUR_DOCKER_NAME -e POSTGRES_PASSWORD=YOUR_PASSWORD -p 5432:5432 -d postgres</code>


# Documentation
When run webserver open browser 

    http://127.0.0.1:8000/redoc
    http://127.0.0.1:8000/docs

