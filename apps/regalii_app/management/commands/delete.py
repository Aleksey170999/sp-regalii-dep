from django.core.management.base import BaseCommand

from apps.regalii_app.models import Regalia, Operation


class Command(BaseCommand):
    def handle(self, *args, **options):
        qs = Regalia.objects.all()
        count = len(qs)
        qs.delete()
        print("\n" + f"Удалено {count} регалий")

        qs = Operation.objects.all()
        count = len(qs)
        qs.delete()
        print("\n" + f"Удалено {count} Операций")
