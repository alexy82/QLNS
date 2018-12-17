from django.db import models


class Promotion(models.Model):
    """
    KHUYENMAI(maKhuyenMai,maCode,dieuKienLon,dieuKienNho,ngayHetHan)
    """
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=16)
    min = models.IntegerField(default=0)
    date_expired = models.DateField()
    money_discount = models.IntegerField(default=0)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return self.code

    def __repr__(self):
        return self.__str__()

    class Meta:
        app_label = "QuanLyNhaSach"
