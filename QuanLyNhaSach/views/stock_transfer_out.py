from rest_framework.viewsets import ModelViewSet
from QuanLyNhaSach.serializers.stock_transfer_out import StockTransferOutDetailSerializer, StockTransferOutSerializer
from QuanLyNhaSach.models.stock_transfer_out import StockTransferOutDetail, StockTransferOut
from datetime import datetime
from QuanLyNhaSach.models.merchandise import Merchandise
from QuanLyNhaSach.models.promotion import Promotion

from QuanLyNhaSach.business_layer.merchandise import MerchandiseHelper

"""
Phiếu xuất kho:
+Thêm
Tồn kho giảm xuống
+Xóa
Tồn kho tăng lên
+Sửa 
Tồn kho có thể giảm xuống hoặc tăng lên
"""


class StockTransferOutViewSet(ModelViewSet):
    queryset = StockTransferOut.objects.all()
    serializer_class = StockTransferOutSerializer

    def perform_create(self, serializer):
        if serializer.is_valid():
            promotion = None
            if 'promotion_code' in self.request.POST:
                promotion_code = self.request.POST['promotion_code']
                if promotion_code is not None and promotion_code != "":
                    promotion = Promotion.objects.get(code=promotion_code)
                    promotion.is_used = True
                    promotion.save()
            serializer.save(created_at=datetime.now(), promotion=promotion)


class StockTransferOutDetailViewSet(ModelViewSet):
    queryset = StockTransferOutDetail.objects.all()
    serializer_class = StockTransferOutDetailSerializer

    def perform_create(self, serializer):
        if serializer.is_valid():
            id_unit = self.request.POST['unit']
            unit = Merchandise.objects.get(pk=id_unit)
            price = unit.price
            unit.available_count -= int(self.request.POST['count'])
            unit.save()
            serializer.save(price=price)

    def perform_update(self, serializer):
        if serializer.is_valid():
            id_detail = self.request.POST['id']
            detail = StockTransferOutDetail.objects.get(pk=id_detail)
            old_unit = detail.unit
            old_unit.available_count += detail.count
            old_unit.save()
            id_unit = self.request.POST['unit']
            unit = Merchandise.objects.get(pk=id_unit)
            unit.available_count -= int(self.request.POST['count'])
            unit.save()
            if detail.unit_id != id_unit:
                price = unit.price
                serializer.save(price=price)
            else:
                serializer.save()

    def perform_destroy(self, instance):
        unit = Merchandise.objects.get(pk=instance.pk)
        unit += instance.count
        unit.save()
