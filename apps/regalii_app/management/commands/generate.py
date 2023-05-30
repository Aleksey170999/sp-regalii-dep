from django.core.management.base import BaseCommand

from apps.regalii_app.generator import RegaliaGenerator
from apps.regalii_app.models import Regalia


class Command(BaseCommand):
    def handle(self, *args, **options):
        qs = Regalia.objects.filter(is_generated=False)
        if qs:
            generator = RegaliaGenerator(qs=qs)
            generator.generate_all()
            archname = generator.save_to_archive()
            print(generator.get_url_to_archive(archname))
        else:
            print('В базе нет записей для генерации регалий')

