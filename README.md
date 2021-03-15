# django-snowflake-sqlalchemy

An example Django application that uses snowflake database  using SqlAlchemy library.

## Project Setup

``` bash
python3 -m venv env

source env/bin/activate

pip install -r requirements.txt

# Now add appropriate snowflake credentials in settings.py
python manage.py sql_alchemy_migrate

python manage.py runserver
```

## Django Settings changes

``` python
# django_snowflake_sqlalchemy/settings.py

from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SNOWFLAKE = {
    'username': 'your_username',
    'password': 'your_password',
    'account': 'your_account',
    'database': 'your_database_name',
    'schema': 'public',
    'warehouse': 'your_warehouse_name',
}
SNOWFLAKE['engine'] = create_engine(
    URL(
        account = SNOWFLAKE['account'],
        user = SNOWFLAKE['username'],
        password = SNOWFLAKE['password'],
        database = SNOWFLAKE['database'],
        schema = SNOWFLAKE['schema'],
        warehouse = SNOWFLAKE['warehouse'],
    ),
    echo=False
)
SNOWFLAKE['session'] = sessionmaker(bind=SNOWFLAKE['engine'])
```

## Using SqlAlchemy session

**Example**
See [this](https://github.com/tysonpaul89/django-snowflake-sqlalchemy/blob/main/crud/views.py) link for the full code.

``` python
# airport/views.py

from .models import Airport # <--- Gets the SqlAlchemy schema
from context_manager.sql_alchemy import session_scope # <--- Importing session.

with session_scope() as session: # <--- Getting session.
    airports = session.query(Airport).all() # <--- Executing query.
    return render(request, 'list_data.html', {'airports': airports})


with session_scope() as session:
    airport = session.query(Airport).get(airport_id)
    if airport:
        session.delete(airport)
        session.commit() # <--- Committing the changes to the session.
```

## Executing Raw SQL

Following example shows the how to execute raw SQL query.

See [this](https://github.com/tysonpaul89/django-snowflake-sqlalchemy/blob/main/crud/views.py) link for the full code.

``` python
# airport/views.py

from django.conf import settings

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
