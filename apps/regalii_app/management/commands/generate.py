from django.core.management.base import BaseCommand

from regalii_app.generator import RegaliaGenerator


class Command(BaseCommand):
    def handle(self, *args, **options):
        generator = RegaliaGenerator()
        generator.generate_png()
