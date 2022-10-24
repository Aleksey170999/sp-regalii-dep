from django.core.management.base import BaseCommand

from regalii_app.importer import RegaliaImporter


class Command(BaseCommand):
    def handle(self, *args, **options):
        importer = RegaliaImporter()
        importer.import_objects()
