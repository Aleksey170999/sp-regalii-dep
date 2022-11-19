from django.core.management.base import BaseCommand

from apps.regalii_app.generator import RegaliaGenerator
from apps.regalii_app.models import Regalia


class Command(BaseCommand):
    def handle(self, *args, **options):
        generator = RegaliaGenerator(qs=Regalia.objects.all())
        generator.generate_all()
