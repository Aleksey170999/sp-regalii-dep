from django.core.management.base import BaseCommand

from regalii_app.uploader import UploadRegalii


class Command(BaseCommand):
    def handle(self, *args, **options):
        uploader = UploadRegalii()
        uploader.upload()
