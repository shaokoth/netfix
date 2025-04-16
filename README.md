## Starting the server

To start the server, run the following commands

Create a virtual environment
```bash
 python3 -m venv venv
```

Activate the virtual environment

```bash
source venv/bin/activate 
```
Install requirements

```bash
 pip install -r requirements.txt
```

Collect/compile static files

```bash
python manage.py collectstatic 
```

Apply all migrations
```bash
python manage.py migrate
```

Start the server
```bash
python3 manage.py runserver
```