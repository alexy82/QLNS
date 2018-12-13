from django.db import models
from random import randint


def generate_code():
    a = [chr(randint(65, 90)) for i in range(8)]
    return "".join(a)


class Promotion(models.Model):
    """
    KHUYENMAI(maKhuyenMai,maCode,dieuKienLon,dieuKienNho,ngayHetHan)
    """
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=16, unique=True, default=generate_code())
    min = models.IntegerField(default=0)
    max = models.IntegerField(default=0)
    date_expired = models.DateField()
    money_discount = models.IntegerField(default=0)
    is_used = models.BooleanField(default=False)

    class Meta:
        app_label = "QuanLyNhaSach"
