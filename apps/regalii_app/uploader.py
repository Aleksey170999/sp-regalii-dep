from datetime import datetime
import yadisk
import yadisk.functions


class UploadRegalii():
    TOKEN = "y0_AgAEA7qjUHgGAAhZ6QAAAADNATw2n8iJTX33SO2FvJTPUxH2Ce4ajtM"
    y = yadisk.YaDisk(token=TOKEN)

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


