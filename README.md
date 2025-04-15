## Starting the server

To start the server, run the following commands
Install requirements

```bash
 pip install -r requirements.txt
```

Activate a virtual environment

```bash
source venv/bin/activate 
```

Collect/compile static files

```bash
python manage.py collectstatic 
```

Start the server
```bash
python3 manage.py runserver
```