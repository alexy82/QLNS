from django.db import models


class CustomerType(models.Model):
    """
    LOAIKHACHHANG(soDiemNho,soDiemLon,loai,mota)
    """
    id = models.AutoField(primary_key=True)
    min = models.IntegerField(default=0, unique=True)
    max = models.IntegerField(default=0, unique=True)
    type = models.CharField(max_length=64)
    descriptions = models.CharField(max_length=256)

    class Meta:
        app_label = "QuanLyNhaSach"


class Customer(models.Model):
    """
    KHACHHANG(maKH,tenKH,soDiem,sdt,diaChi,email)
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=126, null=False, blank=False)
    point = models.IntegerField(default=0)
    phone = models.CharField(max_length=10, blank=True)
    email = models.EmailField(blank=True)
    address = models.CharField(blank=True, max_length=255)

    @property
    def type(self):
        return CustomerType.objects.filter(min__lte=self.point, max__gte=self.point)[0]

    class Meta:
        app_label = "QuanLyNhaSach"
