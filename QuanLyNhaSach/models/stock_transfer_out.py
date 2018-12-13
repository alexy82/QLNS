from django.db import models
from django.contrib.auth.models import User
from QuanLyNhaSach.models.customer import Customer
from QuanLyNhaSach.models.store import Store
from QuanLyNhaSach.models.merchandise import Merchandise
from QuanLyNhaSach.models.promotion import Promotion


class StockTransferOut(models.Model):
    """
    PHIEUXUATKHO(maPhieu,ngayLap,taiKhoan, khachHang,TongTien)
    """
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stock_transfer_out_list')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='stock_transfer_out_list')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='stock_transfer_out_list')
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE, related_name='stock_transfer_out_list',
                                  null=True, blank=True)

    @property
    def total(self):
        total = sum(
            int(i.amount) for i in self.list_detail.all()) - (self.promotion.money_discount if self.promotion else 0)
        return total if total > 0 else total

    class Meta:
        app_label = "QuanLyNhaSach"


class StockTransferOutDetail(models.Model):
    """
    CHITIETPHIEU(maPhieu,maHangHoa, soLuong,thanhTien)
    """
    id = models.AutoField(primary_key=True)
    unit = models.ForeignKey(Merchandise, on_delete=models.CASCADE, related_name="stock_transfer_out_detail_list")
    count = models.IntegerField(default=1)
    price = models.IntegerField(default=0)
    inside = models.ForeignKey(StockTransferOut, on_delete=models.CASCADE, related_name='list_detail')

    @property
    def amount(self):
        return self.price * self.count

    class Meta:
        app_label = "QuanLyNhaSach"
