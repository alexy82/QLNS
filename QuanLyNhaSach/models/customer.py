from django.contrib.auth.models import User
from django.db import models


class CustomerType(models.Model):
    """
    LOAIKHACHHANG(soDiemNho,soDiemLon,loai,mota)
    """
    id = models.AutoField(primary_key=True)
    min = models.IntegerField(default=0, unique=True)
    max = models.IntegerField(default=0, unique=True)
    type = models.CharField(max_length=64, unique=True)
    descriptions = models.CharField(max_length=256)

    def __str__(self):
        return self.type

    def __repr__(self):
        return self.__str__()

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
    user = models.ForeignKey(User, related_name='extend_info', on_delete=models.CASCADE, blank=True,
                             null=True, default=None)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def as_dict(self):
        username = ""
        if self.user is not None:
            username = self.user.username
        return {
            "id": self.id,
            "name": self.name,
            "point": self.point,
            "phone": self.phone,
            "email": self.email,
            "address": self.address,
            "username": username,

        }

    @property
    def type(self):
        query = CustomerType.objects.filter(min__lte=self.point, max__gte=self.point)
        if query.count() == 0:
            return CustomerType(min=0, max=9999999999, type="No Define", descriptions="")
        return query[0]

    class Meta:
        app_label = "QuanLyNhaSach"
