from django.db import models
from django.contrib.auth.models import User
from QuanLyNhaSach.models.supplier import Supplier
from QuanLyNhaSach.models.merchandise import Merchandise


class StockTransferIn(models.Model):
    """
    PHIEUNHAPKHO(maPhieu,ngayLap,taiKhoan, nhaCungCap,tongTien,thanhToan)
    """
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stock_transfer_in_list')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='stock_transfer_in_list')
    paid = models.IntegerField(default=0)

    @property
    def total(self):
        return sum(int(i.amount) for i in self.list_detail.all())

    @property
    def dept(self):
        return self.total - self.paid

    class Meta:
        app_label = "QuanLyNhaSach"


class StockTransferInDetail(models.Model):
    """
    CHITIETPHIEU(maPhieu,maHangHoa, soLuong,thanhTien)
    """
    id = models.AutoField(primary_key=True)
    unit = models.ForeignKey(Merchandise, on_delete=models.CASCADE, related_name="stock_transfer_in_detail_list")
    price = models.IntegerField(default=0)
    count = models.IntegerField(default=1)
    inside = models.ForeignKey(StockTransferIn, on_delete=models.CASCADE, related_name='list_detail')

    @property
    def amount(self):
        return self.price * self.count

    class Meta:
        app_label = "QuanLyNhaSach"
