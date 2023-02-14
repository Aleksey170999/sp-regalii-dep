from django.core.management.base import BaseCommand

from apps.regalii_app.importer import RegaliaImporter


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--f', type=int)

    def handle(self, *args, **options):
        if options["f"]:
            importer = RegaliaImporter(f=options["f"])
            importer.import_objects()
        else:
            importer = RegaliaImporter()
            importer.import_objects()
