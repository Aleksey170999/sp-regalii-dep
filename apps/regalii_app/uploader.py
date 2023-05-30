from datetime import datetime
import yadisk
from django.conf import settings

class UploadRegalii():
    y = yadisk.YaDisk(token=settings.BUCKET_TOKEN)

    def __init__(self):
        pass

    def upload(self):
        print("началась загрузка архива")
        archname = f"archive_{str(datetime.now()).replace(':', '-')[:-7]}"
        try:
            self.y.upload(f"regalii_app/generated/archive.zip", f'/regalii/{archname}.zip')
        except yadisk.exceptions.PathExistsError:
            pass
        print("\nАрхив загружен на яндек диск:")
