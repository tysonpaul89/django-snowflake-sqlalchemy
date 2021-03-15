# django-snowflake-sqlalchemy

This is an example django application that uses snowflake database with SqlAlchemy library.

## Project Setup

``` bash
python3 -m venv env

source env/bin/activate

pip install -r requirements.txt

# Now add appropriate snowflake credentials in settings.py
python manage.py sql_alchemy_migrate

python manage.py runserver
```
## Using SqlAlchemy session

**Example**
See [this](https://github.com/tysonpaul89/django-snowflake-sqlalchemy/blob/main/crud/views.py) link for the full code.

``` python
# crud/views.py

from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from .models import Airport
from context_manager.sql_alchemy import session_scope # <--- Importing session.

def list_data(request):
    """Function to list data using SQLAlchemy ORM"""

    with session_scope() as session: # <--- Getting session.
        airports = session.query(Airport).all() # <--- Executing query.
        return render(request, 'list_data.html', {'airports': airports})

def delete_data(request, airport_id):
    """Function to delete data using SQLAlchemy ORM"""

    with session_scope() as session:
        try:
            airport = session.query(Airport).get(airport_id)
            if airport:
                session.delete(airport)
                session.commit() # <--- Committing the changes to the session.
                messages.success(request, 'Airport data deleted successfully.')
            else:
                messages.error(request, 'Airport not found!')
        except:
            messages.error(request, 'Sorry! An error occurred. Airport data not deleted.')

        return redirect(reverse('list_data'))
```

## Executing Raw SQL

Following example shows the how to execute raw SQL query.

See [this](https://github.com/tysonpaul89/django-snowflake-sqlalchemy/blob/main/crud/views.py) link for the full code.

``` python
def list_data_using_raw_sql(request):
    """Example method to show raw SQL execution"""

    engine = settings.SNOWFLAKE['engine']
    connection = engine.connect()

    try:
        engine = settings.SNOWFLAKE['engine']
        connection = engine.connect()
        cursor = connection.execute("SELECT * FROM airport")
        airports = cursor.fetchall()
        return render(request, 'list_data.html', {'airports': airports})
    finally:
        connection.close()
        engine.dispose()
```