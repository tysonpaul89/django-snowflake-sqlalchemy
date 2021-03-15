from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from crud.models import Base

class Command(BaseCommand):
    help = 'Migrates SQLAlchemy mapping classes'

    def handle(self, *args, **options):
        try:
            Base.metadata.create_all(settings.SNOWFLAKE['engine'])
            self.stdout.write(self.style.SUCCESS('Mapping classes migrated successfully.'))
        except Exception as error:
            self.stdout.write(self.style.ERROR(error))
