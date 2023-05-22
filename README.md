# NG-CDF Website

The NG-CDF website manages government-funded projects and bursaries. It offers an admin interface for project management, bursary applications, and reporting. Visitors can access project details, track progress, apply for bursaries, and communicate with the government. The website promotes transparency, efficiency, and stakeholder engagement, benefiting constituents and communities.

# Installation 
Create a virtual environment e.g with `virtualenv`
```bash
pip install virtualenv
virtualenv venv
```

Activate the virtual environment
In linux
```bash
source venv/bin/activate
```

```bash
venv\Scripts\activate
```

Instal the requirements from the `requirements.txt` file

```bash
pip install  -r requirements.txt
```

Set up the necessary environment variables in a .env file
```
DB_NAME='ng_cdf_db'
DB_USER=''
DB_PASS=''
DB_HOST=''
BD_PORT=5432
```

run
```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

```bash
python manage.py runserver
```

The development server should be running on `localhost`, the default port is `8000`