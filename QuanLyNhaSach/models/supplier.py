from datetime import datetime
from django.db import models

"""
NHACUNGCAP (maNCC,tenNCC , ngayKyHopDong,sdt,email,diaChi)
"""


class Supplier(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, blank=False)
    cooperation_date = models.DateField(blank=False)
    phone = models.CharField(max_length=10, blank=True)
    email = models.EmailField(blank=True)
    address = models.CharField(blank=True, max_length=255)

    class Meta:
        app_label = "QuanLyNhaSach"
