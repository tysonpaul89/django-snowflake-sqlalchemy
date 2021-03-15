from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from .models import Airport
from .forms import AirportForm
from context_manager.sql_alchemy import session_scope

def list_data(request):
    """Function to list data using SQLAlchemy ORM"""

    with session_scope() as session:
        airports = session.query(Airport).all()
        return render(request, 'list_data.html', {'airports': airports})

def create_data(request):
    """Function to create data using SQLAlchemy ORM"""

    if request.method == 'POST':
        form = AirportForm(request.POST)
        if form.is_valid():
            with session_scope() as session:
                try:
                    airport = Airport()
                    airport.name = form.cleaned_data['name']
                    airport.airport_code = form.cleaned_data['code']
                    airport.location = form.cleaned_data['location']
                    session.add(airport)
                    session.commit()

                    messages.success(request, 'Airport data deleted successfully.')
                except:
                    messages.error(request, 'Sorry! An error occurred. Airport data not saved.')

            return redirect(reverse('list_data'))
    else:
        form = AirportForm()

    return render(request, 'create_data.html', {'form': form})

def delete_data(request, airport_id):
    """Function to delete data using SQLAlchemy ORM"""

    with session_scope() as session:
        try:
            airport = session.query(Airport).get(airport_id)
            if airport:
                session.delete(airport)
                session.commit()
                messages.success(request, 'Airport data deleted successfully.')
            else:
                messages.error(request, 'Airport not found!')
        except:
            messages.error(request, 'Sorry! An error occurred. Airport data not deleted.')

        return redirect(reverse('list_data'))

def update_data(request, airport_id):
    """Function to delete data using SQLAlchemy ORM"""

    with session_scope() as session:
        try:
            airport = session.query(Airport).get(airport_id)
            if airport:
                if request.method == 'POST':
                    form = AirportForm(request.POST)
                    if form.is_valid():
                        airport.name = form.cleaned_data['name']
                        airport.airport_code = form.cleaned_data['code']
                        airport.location = form.cleaned_data['location']
                        session.commit()

                        messages.success(request, 'Airport data updated successfully.')

                        return redirect(reverse('list_data'))
                else:
                    form = AirportForm(initial={
                        'name': airport.name,
                        'code': airport.airport_code,
                        'location': airport.location,
                    })

                return render(request, 'update_data.html', {'form': form, 'airport': airport})
            else:
                messages.error(request, 'Airport not found!')
        except:
            messages.error(request, 'Sorry! An error occurred. Airport data not updated.')

        return redirect(reverse('list_data'))

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