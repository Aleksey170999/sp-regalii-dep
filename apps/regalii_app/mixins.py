import uuid

from django.db import models


class UidModel(models.Model):
    """
    Объект с уникальным идентификатором
    """
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True


class UidPrimaryModel(models.Model):
    """
    Объект с UUID первичным ключём
    """
    uid = models.UUIDField('UID', default=uuid.uuid4, editable=False, primary_key=True)

    class Meta:
        abstract = True
