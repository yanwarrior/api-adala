# API Adala
This is the `Adala API`, an application for `B2B E-commerce`.
This API will be consumed by the `Adale Web` (Frontend App).


## Quick Setup
Before you install the need for this API, you need to set up
a PostgreSQL database with the name `db_adala`.

After that follow the steps below. I recommend using
`Virtual Environment`:
```
(.venv) $ pip install -r requirements.txt
```

Migrate data:
```
(.venv) $ python manage.py migrate
```

If necessary, you can create an admin user:
```
(.venv) $ python manage.py createsuperuser
```

Run the development server:
```
(.venv) $ python manage.py runserver
```

