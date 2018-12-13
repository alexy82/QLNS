from django.db import models


class Store(models.Model):
    """
    CUAHANG(maCuaHang,tenCuaHang,sdt,diaChi)
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=256)

    class Meta:
        app_label = "QuanLyNhaSach"
