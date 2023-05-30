from datetime import datetime
import os
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from django.conf import settings

import boto3

from apps.regalii_app.utils import prepare_text, draw_text


class RegaliaGenerator:
    sizes = [(315, 177), (272, 98), (320, 107), (320, 80)]

    def __init__(self, qs=None, ins=None):
        self.qs = qs
        self.ins = ins

    def generate_one(self, ins):
        for size in self.sizes:
            font = ImageFont.truetype('regalii/helios.ttf', 23, encoding="utf-8") if size == (
                315, 177) else ImageFont.truetype('regalii/helios.ttf', 19, encoding="utf-8")
            im = Image.new('RGB', size, (232, 243, 249))
            self.generate_png(im=im, ins=ins, font=font, size=size)

    def generate_all(self):
        counter = 0
        for ins in self.qs:
            self.generate_one(ins)
            counter += 1
            ins.is_generated = True
            ins.save()
            print(ins.full_name)

    def generate_png(self, im, ins, font, size):
        draw = ImageDraw.Draw(im)
        data = self._get_data(ins)
        text = prepare_text(data)
        draw_text(text=text, font=font, draw=draw, size=size)
        self.save_png(data, im)

    def _get_data(self, ins):
        fio = ins.full_name
        rank = ins.rank
        city = ins.city
        fir_name = ins.first_name
        sec_name = ins.second_name
        thi_name = ins.third_name if ins.third_name != '' else None
        en_regalia = ins.en_regalia
        ru_regalia = ins.regalia

        data = {"fio": fio,
                "rank": rank,
                "city": city,
                "fir_name": fir_name,
                "sec_name": sec_name,
                "thi_name": thi_name,
                "en_regalia": en_regalia,
                "ru_regalia": ru_regalia}

        return data


    def save_png(self, data, im):
        path = f'/{settings.REGALII_DIR}/'

        if im.size == (315, 177):
            i = 1
        if im.size == (272, 98):
            i = 2
        if im.size == (320, 107):
            i = 3
        if im.size == (320, 80):
            i = 4
        name = f'{data["sec_name"]}_{data["fir_name"][0]}{data["thi_name"][0]}_{i}.png' if data[
            "thi_name"] else f'{data["sec_name"]}_{data["fir_name"][0]}_{i}.png'
        if name in os.listdir(settings.REGALII_DIR):
            name = f'{data["sec_name"]}_{data["fir_name"][0]}{data["thi_name"][0]}_{i}.png' if data[
            "thi_name"] else f'{data["sec_name"]}_{data["fir_name"][0]}_{i}_.png'
        im.save(path + name)

    def save_to_archive(self):
        archname = f'regalii_{datetime.now()}.zip'

        folder_to_compress = Path(settings.REGALII_DIR)
        path_to_archive = Path(settings.ARCHIVES_DIR / archname)

        with zipfile.ZipFile(
                path_to_archive,
                mode="w",
                compression=zipfile.ZIP_DEFLATED,
                compresslevel=7,
        ) as zip:
            for file in folder_to_compress.rglob("*"):
                relative_path = file.relative_to(folder_to_compress)
                zip.write(file, arcname=relative_path)
                os.remove(settings.REGALII_DIR.joinpath(file))
        return archname

    def get_url_to_archive(self, archname):
        file = settings.ARCHIVES_DIR.joinpath(archname)

        s3 = boto3.client(service_name=settings.SERVICE_NAME,
                          region_name=settings.REGION_NAME,
                          aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                          endpoint_url=settings.ENDPOINT_URL)

        s3.upload_file(str(file), 'sp-at', f'regalii/{archname}')
        url = s3.generate_presigned_url('get_object',
                                        Params={'Bucket': 'sp-at',
                                                'Key': f'regalii/{archname}'})
        return url
