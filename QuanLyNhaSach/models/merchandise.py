from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class MerchandiseType(models.Model):
    """
    CHITIETLOAI(maChiTietLoai, loai, moTa)
    """

    id = models.AutoField(primary_key=True)
    type_for = models.IntegerField(blank=False, default=0, validators=[
        MaxValueValidator(1),
        MinValueValidator(0)
    ])
    type_name = models.CharField(max_length=64, blank=False)
    description = models.CharField(max_length=256)

    def __str__(self):
        return self.type_name

    def __repr__(self):
        return self.__str__()

    class Meta:
        app_label = "QuanLyNhaSach"


class Merchandise(models.Model):
    """
    HANGHOA(maHang,maLoaiHang,DonGia,TenHang,maChiTietLoai,SoLuongTon,ThongTinThem)
    """
    id = models.AutoField(primary_key=True)
    # 0 văn phòng phẩm, 1: Sách
    merchandise_type = models.IntegerField(blank=False, default=0, validators=[
        MaxValueValidator(1),
        MinValueValidator(0)
    ])
    price = models.IntegerField(default=0, validators=[
        MinValueValidator(0)
    ])
    picture = models.CharField(max_length=512, default="")
    name = models.CharField(blank=False, max_length=128, null=False)
    type = models.ForeignKey(MerchandiseType, on_delete=models.CASCADE)
    available_count = models.IntegerField(default=0)
    more_info = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    class Meta:
        app_label = "QuanLyNhaSach"
